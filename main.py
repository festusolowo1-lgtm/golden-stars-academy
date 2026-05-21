from fastapi import FastAPI, Request, Form, File, UploadFile, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlmodel import SQLModel, Field, Session, create_engine, select
import bcrypt
from typing import Optional
from datetime import datetime
from pathlib import Path
import uuid, os, shutil

# ── CONFIG ──────────────────────────────────────────────────────
SECRET_KEY   = os.getenv("SECRET_KEY", "gsa-fastapi-secret-2026")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///gsa.db")
UPLOAD_DIR   = Path("static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_EXT  = {"png","jpg","jpeg","gif","webp","svg"}

engine = create_engine(DATABASE_URL, echo=False)
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

app = FastAPI(title="Golden Stars Academy")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY, max_age=86400)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ── MODELS ──────────────────────────────────────────────────────

class User(SQLModel, table=True):
    __tablename__ = "user"
    id:       Optional[int] = Field(default=None, primary_key=True)
    name:     str
    email:    str           = Field(unique=True, index=True)
    password: str
    role:     str           = Field(default="ict")
    status:   str           = Field(default="active")
    avatar:   str           = Field(default="")
    created:  str           = Field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d"))

class SiteInfo(SQLModel, table=True):
    __tablename__ = "siteinfo"
    id:    Optional[int] = Field(default=None, primary_key=True)
    key:   str           = Field(unique=True, index=True)
    value: str           = Field(default="")

class News(SQLModel, table=True):
    __tablename__ = "news"
    id:        Optional[int] = Field(default=None, primary_key=True)
    title:     str
    body:      str
    image_url: str  = Field(default="")
    published: bool = Field(default=True)
    author:    str  = Field(default="")
    date:      str  = Field(default="")
    created:   str  = Field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d %H:%M"))

class Fee(SQLModel, table=True):
    __tablename__ = "fee"
    id:         Optional[int] = Field(default=None, primary_key=True)
    level:      str
    term:       str
    session:    str
    amount:     float
    status:     str = Field(default="pending")
    updated_by: str = Field(default="")
    updated_at: str = Field(default="")

class GalleryItem(SQLModel, table=True):
    __tablename__ = "galleryitem"
    id:          Optional[int] = Field(default=None, primary_key=True)
    title:       str
    category:    str
    url:         str = Field(default="")
    role:        str = Field(default="")
    bio:         str = Field(default="")
    uploaded_by: str = Field(default="")
    date:        str = Field(default="")
    created:     str = Field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d %H:%M"))

class CalendarEvent(SQLModel, table=True):
    __tablename__ = "calendarevent"
    id:      Optional[int] = Field(default=None, primary_key=True)
    type:    str
    title:   str
    date:    str
    note:    str = Field(default="")
    created: str = Field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d %H:%M"))

class Logo(SQLModel, table=True):
    __tablename__ = "logo"
    id:         Optional[int] = Field(default=None, primary_key=True)
    logo_type:  str           = Field(unique=True)
    url:        str           = Field(default="")
    alt_text:   str           = Field(default="")
    updated_by: str           = Field(default="")
    updated_at: str           = Field(default="")

# ── DB HELPERS ───────────────────────────────────────────────────

def get_db():
    with Session(engine) as s:
        yield s

def get_info(db: Session, key: str, default: str = "") -> str:
    row = db.exec(select(SiteInfo).where(SiteInfo.key == key)).first()
    return row.value if row else default

def set_info(db: Session, key: str, value: str):
    row = db.exec(select(SiteInfo).where(SiteInfo.key == key)).first()
    if row:
        row.value = value
        db.add(row)
    else:
        db.add(SiteInfo(key=key, value=value))
    db.commit()

def save_upload(file: UploadFile) -> str:
    if not file or not file.filename:
        return ""
    ext = file.filename.rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_EXT:
        return ""
    fname = f"{uuid.uuid4().hex}.{ext}"
    path  = UPLOAD_DIR / fname
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return f"/static/uploads/{fname}"

def make_avatar(name: str) -> str:
    parts = name.strip().split()
    return "".join(p[0] for p in parts[:2]).upper()

# ── AUTH HELPERS ─────────────────────────────────────────────────

def get_current_user(request: Request, db: Session = Depends(get_db)) -> Optional[User]:
    uid = request.session.get("user_id")
    if not uid:
        return None
    return db.exec(select(User).where(User.id == uid)).first()

def require_login(request: Request, db: Session = Depends(get_db)) -> User:
    user = get_current_user(request, db)
    if not user or user.status != "active":
        raise HTTPException(status_code=302, headers={"Location": "/admin/login"})
    return user

def require_role(*roles):
    def dep(request: Request, db: Session = Depends(get_db)) -> User:
        user = get_current_user(request, db)
        if not user or user.status != "active":
            raise HTTPException(302, headers={"Location": "/admin/login"})
        if user.role not in roles:
            raise HTTPException(302, headers={"Location": "/admin?err=access"})
        return user
    return dep

def flash(request: Request, msg: str, cat: str = "success"):
    msgs = request.session.get("flash", [])
    msgs.append({"cat": cat, "msg": msg})
    request.session["flash"] = msgs

def get_flash(request: Request):
    msgs = request.session.pop("flash", [])
    return msgs

def ctx(request: Request, db: Session, **kw):
    """Base template context."""
    school_logo   = db.exec(select(Logo).where(Logo.logo_type == "school")).first()
    designer_logo = db.exec(select(Logo).where(Logo.logo_type == "webdesigner")).first()
    return {
        "request":       request,
        "current_user":  get_current_user(request, db),
        "school_logo":   school_logo,
        "designer_logo": designer_logo,
        "flash_msgs":    get_flash(request),
        **kw,
    }

# ── STARTUP ──────────────────────────────────────────────────────

@app.on_event("startup")
def startup():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as db:
        if not db.exec(select(User).where(User.role == "superadmin")).first():
            db.add(User(
                name="Daniel Ayo David",
                email="admin@goldenstarsacademy.com",
                password=hash_password("GoldenStars@2026"),
                role="superadmin", status="active", avatar="DA"
            ))
            db.commit()
            print("✅ Super Admin seeded: admin@goldenstarsacademy.com / GoldenStars@2026")

# ═══════════════════════════════════════════════════════════════
# PUBLIC ROUTES
# ═══════════════════════════════════════════════════════════════

@app.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    news = db.exec(select(News).where(News.published == True).order_by(News.id.desc()).limit(3)).all()
    return templates.TemplateResponse("index.html", ctx(request, db, news=news,
        site={k: get_info(db, k, v) for k, v in {
            "phone1":"+234 803 442 8823","phone2":"+234 807 936 6268",
            "email":"info@goldenstarsacademy.com",
            "address":"Q762, After Living Faith Church, Yetu Quarters, GRA Gbessa, Abuja",
            "tagline":"God is Able · GRA Gbessa, Abuja",
            "facebook":"","instagram":"","whatsapp":""
        }.items()}
    ))

# ── JSON APIs ─────────────────────────────────────────────────

@app.get("/api/news")
def api_news(db: Session = Depends(get_db)):
    return [{"id":n.id,"title":n.title,"body":n.body,"date":n.date,"image_url":n.image_url}
            for n in db.exec(select(News).where(News.published==True).order_by(News.id.desc())).all()]

@app.get("/api/fees")
def api_fees(db: Session = Depends(get_db)):
    return [{"level":f.level,"term":f.term,"session":f.session,"amount":f.amount}
            for f in db.exec(select(Fee).where(Fee.status=="approved")).all()]

@app.get("/api/gallery")
def api_gallery(db: Session = Depends(get_db)):
    return [{"id":g.id,"title":g.title,"category":g.category,"url":g.url,"role":g.role,"bio":g.bio}
            for g in db.exec(select(GalleryItem).order_by(GalleryItem.id.desc())).all()]

@app.get("/api/calendar")
def api_calendar(db: Session = Depends(get_db)):
    return [{"type":c.type,"title":c.title,"date":c.date,"note":c.note}
            for c in db.exec(select(CalendarEvent).order_by(CalendarEvent.date)).all()]

@app.get("/api/siteinfo")
def api_siteinfo(db: Session = Depends(get_db)):
    keys = ["phone1","phone2","email","address","tagline","facebook","instagram","whatsapp"]
    return {k: get_info(db, k) for k in keys}

@app.get("/api/logos")
def api_logos(db: Session = Depends(get_db)):
    s = db.exec(select(Logo).where(Logo.logo_type=="school")).first()
    d = db.exec(select(Logo).where(Logo.logo_type=="webdesigner")).first()
    return {
        "school":   {"url": s.url if s else "", "alt": s.alt_text if s else "Golden Stars Academy"},
        "designer": {"url": d.url if d else "", "alt": d.alt_text if d else "Eled Global"},
    }

# ═══════════════════════════════════════════════════════════════
# AUTH
# ═══════════════════════════════════════════════════════════════

@app.get("/admin/login", response_class=HTMLResponse)
def login_page(request: Request, db: Session = Depends(get_db)):
    if request.session.get("user_id"):
        return RedirectResponse("/admin", 302)
    return templates.TemplateResponse("admin/login.html", ctx(request, db))

@app.post("/admin/login", response_class=HTMLResponse)
def login_post(request: Request, db: Session = Depends(get_db),
               email: str = Form(...), password: str = Form(...)):
    user = db.exec(select(User).where(User.email == email)).first()
    if user and user.status == "active" and verify_password(password, user.password):
        request.session["user_id"] = user.id
        return RedirectResponse("/admin", 302)
    flash(request, "Invalid credentials or inactive account.", "error")
    return RedirectResponse("/admin/login", 302)

@app.get("/admin/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/admin/login", 302)

# ═══════════════════════════════════════════════════════════════
# ADMIN DASHBOARD
# ═══════════════════════════════════════════════════════════════

@app.get("/admin", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db),
              user: User = Depends(require_login)):
    err = request.query_params.get("err")
    pending_results = db.exec(select(ExamResult).where(ExamResult.approved == False)).all()
    counts = {
        "users":           len(db.exec(select(User)).all()),
        "staff":           len(db.exec(select(StaffUser)).all()),
        "students":        len(db.exec(select(Student)).all()),
        "parents":         len(db.exec(select(ParentUser)).all()),
        "news":            len(db.exec(select(News)).all()),
        "fees":            len(db.exec(select(Fee)).all()),
        "gallery":         len(db.exec(select(GalleryItem)).all()),
        "calendar":        len(db.exec(select(CalendarEvent)).all()),
        "pending_results": len(pending_results),
    }
    recent_news = db.exec(select(News).order_by(News.id.desc()).limit(5)).all()
    pending_fees = db.exec(select(Fee).where(Fee.status=="pending")).all()
    return templates.TemplateResponse("admin/dashboard.html",
        ctx(request, db, counts=counts, recent_news=recent_news,
            pending_fees=pending_fees, access_error=err=="access",
            pending_results_count=len(pending_results)))

# ═══════════════════════════════════════════════════════════════
# USERS  (Super Admin only)
# ═══════════════════════════════════════════════════════════════

@app.get("/admin/users", response_class=HTMLResponse)
def users_list(request: Request, db: Session = Depends(get_db),
               user: User = Depends(require_role("superadmin"))):
    users = db.exec(select(User).order_by(User.id)).all()
    return templates.TemplateResponse("admin/users.html", ctx(request, db, users=users))

@app.get("/admin/users/create", response_class=HTMLResponse)
def user_create_page(request: Request, db: Session = Depends(get_db),
                     user: User = Depends(require_role("superadmin"))):
    return templates.TemplateResponse("admin/user_form.html", ctx(request, db, item=None))

@app.post("/admin/users/create")
def user_create_post(request: Request, db: Session = Depends(get_db),
                     user: User = Depends(require_role("superadmin")),
                     name: str = Form(...), email: str = Form(...),
                     password: str = Form(...), role: str = Form(...)):
    if db.exec(select(User).where(User.email == email)).first():
        flash(request, "Email already exists.", "error")
    else:
        db.add(User(name=name, email=email,
                    password=hash_password(password),
                    role=role, avatar=make_avatar(name)))
        db.commit()
        flash(request, f"User '{name}' created successfully.")
    return RedirectResponse("/admin/users", 302)

@app.post("/admin/users/{uid}/toggle")
def user_toggle(uid: int, request: Request, db: Session = Depends(get_db),
                user: User = Depends(require_role("superadmin"))):
    u = db.get(User, uid)
    if u and u.role != "superadmin":
        u.status = "inactive" if u.status == "active" else "active"
        db.add(u); db.commit()
        flash(request, f"User status updated to {u.status}.")
    return RedirectResponse("/admin/users", 302)

@app.post("/admin/users/{uid}/delete")
def user_delete(uid: int, request: Request, db: Session = Depends(get_db),
                user: User = Depends(require_role("superadmin"))):
    u = db.get(User, uid)
    if u and u.role != "superadmin":
        db.delete(u); db.commit()
        flash(request, "User deleted.")
    return RedirectResponse("/admin/users", 302)

# ═══════════════════════════════════════════════════════════════
# LOGOS
# ═══════════════════════════════════════════════════════════════

@app.get("/admin/logos", response_class=HTMLResponse)
def logos_page(request: Request, db: Session = Depends(get_db),
               user: User = Depends(require_role("superadmin","ict"))):
    school   = db.exec(select(Logo).where(Logo.logo_type=="school")).first()
    designer = db.exec(select(Logo).where(Logo.logo_type=="webdesigner")).first()
    return templates.TemplateResponse("admin/logos.html",
        ctx(request, db, school=school, designer=designer))

@app.post("/admin/logos")
async def logos_post(request: Request, db: Session = Depends(get_db),
                     user: User = Depends(require_role("superadmin","ict")),
                     logo_type: str = Form(...), alt_text: str = Form(""),
                     logo_url:  str = Form(""),
                     logo_file: UploadFile = File(None)):
    url = save_upload(logo_file) or logo_url
    logo = db.exec(select(Logo).where(Logo.logo_type==logo_type)).first()
    if logo:
        logo.url=url; logo.alt_text=alt_text
        logo.updated_by=user.name; logo.updated_at=datetime.utcnow().strftime("%Y-%m-%d")
        db.add(logo)
    else:
        db.add(Logo(logo_type=logo_type, url=url, alt_text=alt_text,
                    updated_by=user.name, updated_at=datetime.utcnow().strftime("%Y-%m-%d")))
    db.commit()
    flash(request, f"{logo_type.title()} logo updated.")
    return RedirectResponse("/admin/logos", 302)

# ═══════════════════════════════════════════════════════════════
# ADD THESE NEW MODELS to main.py  (after the Logo model)
# ═══════════════════════════════════════════════════════════════

class Student(SQLModel, table=True):
    __tablename__ = "student"
    id:           Optional[int] = Field(default=None, primary_key=True)
    full_name:    str
    admission_no: str            = Field(default="", unique=True, index=True)
    class_name:   str            = Field(default="")   # e.g. "JSS 1A"
    level:        str            = Field(default="")   # JSS | SSS | Primary
    gender:       str            = Field(default="")
    parent_email: str            = Field(default="")
    parent_phone: str            = Field(default="")
    session:      str            = Field(default="2025/2026")
    added_by:     str            = Field(default="")
    created:      str            = Field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d"))

class StaffUser(SQLModel, table=True):
    __tablename__ = "staffuser"
    id:         Optional[int] = Field(default=None, primary_key=True)
    name:       str
    email:      str           = Field(unique=True, index=True)
    password:   str
    role:       str           = Field(default="teacher")  # teacher | headteacher | principal
    subject:    str           = Field(default="")
    class_name: str           = Field(default="")         # form teacher class
    section:    str           = Field(default="")         # Primary | Secondary
    status:     str           = Field(default="active")
    created:    str           = Field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d"))

class Assignment(SQLModel, table=True):
    __tablename__ = "assignment"
    id:           Optional[int] = Field(default=None, primary_key=True)
    title:        str
    description:  str           = Field(default="")
    subject:      str           = Field(default="")
    class_name:   str           = Field(default="")
    due_date:     str           = Field(default="")
    created_by:   str           = Field(default="")
    teacher_id:   int           = Field(default=0)
    session:      str           = Field(default="2025/2026")
    term:         str           = Field(default="Third Term")
    created:      str           = Field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d %H:%M"))

class AssignmentSubmission(SQLModel, table=True):
    __tablename__ = "assignmentsubmission"
    id:            Optional[int] = Field(default=None, primary_key=True)
    assignment_id: int           = Field(default=0, index=True)
    student_id:    int           = Field(default=0, index=True)
    student_name:  str           = Field(default="")
    content:       str           = Field(default="")   # text answer
    file_url:      str           = Field(default="")   # uploaded file
    grade:         str           = Field(default="")   # e.g. A, B+, 85
    feedback:      str           = Field(default="")
    status:        str           = Field(default="submitted")  # submitted|graded
    submitted_at:  str           = Field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d %H:%M"))

class ExamResult(SQLModel, table=True):
    __tablename__ = "examresult"
    id:           Optional[int] = Field(default=None, primary_key=True)
    student_id:   int           = Field(default=0, index=True)
    student_name: str           = Field(default="")
    admission_no: str           = Field(default="")
    class_name:   str           = Field(default="")
    subject:      str           = Field(default="")
    ca1:          float         = Field(default=0.0)
    ca2:          float         = Field(default=0.0)
    exam:         float         = Field(default=0.0)
    total:        float         = Field(default=0.0)
    grade:        str           = Field(default="")
    remark:       str           = Field(default="")
    term:         str           = Field(default="Third Term")
    session:      str           = Field(default="2025/2026")
    uploaded_by:  str           = Field(default="")
    approved:     bool          = Field(default=False)  # Principal/Admin must approve
    created:      str           = Field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d"))

class ParentUser(SQLModel, table=True):
    __tablename__ = "parentuser"
    id:           Optional[int] = Field(default=None, primary_key=True)
    name:         str
    email:        str           = Field(unique=True, index=True)
    password:     str
    phone:        str           = Field(default="")
    student_ids:  str           = Field(default="")  # comma-separated student IDs
    status:       str           = Field(default="active")
    created:      str           = Field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d"))

# ═══════════════════════════════════════════════════════════════
# NEWS
# ═══════════════════════════════════════════════════════════════

@app.get("/admin/news", response_class=HTMLResponse)
def news_list(request: Request, db: Session = Depends(get_db),
              user: User = Depends(require_role("superadmin","ict"))):
    items = db.exec(select(News).order_by(News.id.desc())).all()
    return templates.TemplateResponse("admin/news.html", ctx(request, db, items=items))

@app.get("/admin/news/create", response_class=HTMLResponse)
def news_create_page(request: Request, db: Session = Depends(get_db),
                     user: User = Depends(require_role("superadmin","ict"))):
    return templates.TemplateResponse("admin/news_form.html", ctx(request, db, item=None))

@app.post("/admin/news/create")
async def news_create_post(request: Request, db: Session = Depends(get_db),
                           user: User = Depends(require_role("superadmin","ict")),
                           title: str = Form(...), body: str = Form(...),
                           published: str = Form(""), image: UploadFile = File(None)):
    db.add(News(title=title, body=body, image_url=save_upload(image),
                published=bool(published), author=user.name,
                date=datetime.utcnow().strftime("%Y-%m-%d")))
    db.commit()
    flash(request, "News post created.")
    return RedirectResponse("/admin/news", 302)

@app.get("/admin/news/{nid}/edit", response_class=HTMLResponse)
def news_edit_page(nid: int, request: Request, db: Session = Depends(get_db),
                   user: User = Depends(require_role("superadmin","ict"))):
    return templates.TemplateResponse("admin/news_form.html",
        ctx(request, db, item=db.get(News, nid)))

@app.post("/admin/news/{nid}/edit")
async def news_edit_post(nid: int, request: Request, db: Session = Depends(get_db),
                         user: User = Depends(require_role("superadmin","ict")),
                         title: str = Form(...), body: str = Form(...),
                         published: str = Form(""), image: UploadFile = File(None)):
    n = db.get(News, nid)
    if n:
        n.title=title; n.body=body; n.published=bool(published)
        img = save_upload(image)
        if img: n.image_url = img
        db.add(n); db.commit()
        flash(request, "News updated.")
    return RedirectResponse("/admin/news", 302)

@app.post("/admin/news/{nid}/delete")
def news_delete(nid: int, request: Request, db: Session = Depends(get_db),
                user: User = Depends(require_role("superadmin","ict"))):
    n = db.get(News, nid)
    if n: db.delete(n); db.commit()
    flash(request, "News deleted.")
    return RedirectResponse("/admin/news", 302)

# ═══════════════════════════════════════════════════════════════
# FEES
# ═══════════════════════════════════════════════════════════════

@app.get("/admin/fees", response_class=HTMLResponse)
def fees_list(request: Request, db: Session = Depends(get_db),
              user: User = Depends(require_role("superadmin","bursar"))):
    items = db.exec(select(Fee).order_by(Fee.id.desc())).all()
    return templates.TemplateResponse("admin/fees.html", ctx(request, db, items=items))

@app.get("/admin/fees/create", response_class=HTMLResponse)
def fee_create_page(request: Request, db: Session = Depends(get_db),
                    user: User = Depends(require_role("superadmin","bursar"))):
    return templates.TemplateResponse("admin/fee_form.html", ctx(request, db, item=None))

@app.post("/admin/fees/create")
def fee_create_post(request: Request, db: Session = Depends(get_db),
                    user: User = Depends(require_role("superadmin","bursar")),
                    level: str=Form(...), term: str=Form(...), session: str=Form(...),
                    amount: float=Form(...), status: str=Form("pending")):
    db.add(Fee(level=level, term=term, session=session, amount=amount,
               status=status, updated_by=user.name,
               updated_at=datetime.utcnow().strftime("%Y-%m-%d")))
    db.commit()
    flash(request, "Fee entry created.")
    return RedirectResponse("/admin/fees", 302)

@app.get("/admin/fees/{fid}/edit", response_class=HTMLResponse)
def fee_edit_page(fid: int, request: Request, db: Session = Depends(get_db),
                  user: User = Depends(require_role("superadmin","bursar"))):
    return templates.TemplateResponse("admin/fee_form.html",
        ctx(request, db, item=db.get(Fee, fid)))

@app.post("/admin/fees/{fid}/edit")
def fee_edit_post(fid: int, request: Request, db: Session = Depends(get_db),
                  user: User = Depends(require_role("superadmin","bursar")),
                  level:str=Form(...), term:str=Form(...), session:str=Form(...),
                  amount:float=Form(...), status:str=Form("pending")):
    f = db.get(Fee, fid)
    if f:
        f.level=level; f.term=term; f.session=session
        f.amount=amount; f.status=status
        f.updated_by=user.name; f.updated_at=datetime.utcnow().strftime("%Y-%m-%d")
        db.add(f); db.commit()
        flash(request, "Fee updated.")
    return RedirectResponse("/admin/fees", 302)

@app.post("/admin/fees/{fid}/approve")
def fee_approve(fid: int, request: Request, db: Session = Depends(get_db),
                user: User = Depends(require_role("superadmin"))):
    f = db.get(Fee, fid)
    if f: f.status="approved"; db.add(f); db.commit()
    flash(request, "Fee approved and published to website.")
    return RedirectResponse("/admin/fees", 302)

@app.post("/admin/fees/{fid}/delete")
def fee_delete(fid: int, request: Request, db: Session = Depends(get_db),
               user: User = Depends(require_role("superadmin"))):
    f = db.get(Fee, fid)
    if f: db.delete(f); db.commit()
    flash(request, "Fee deleted.")
    return RedirectResponse("/admin/fees", 302)

# ═══════════════════════════════════════════════════════════════
# GALLERY / TEAM
# ═══════════════════════════════════════════════════════════════

@app.get("/admin/gallery", response_class=HTMLResponse)
def gallery_list(request: Request, db: Session = Depends(get_db),
                 user: User = Depends(require_role("superadmin","media","ict"))):
    items = db.exec(select(GalleryItem).order_by(GalleryItem.id.desc())).all()
    return templates.TemplateResponse("admin/gallery.html", ctx(request, db, items=items))

@app.get("/admin/gallery/upload", response_class=HTMLResponse)
def gallery_upload_page(request: Request, db: Session = Depends(get_db),
                        user: User = Depends(require_role("superadmin","media","ict"))):
    return templates.TemplateResponse("admin/gallery_form.html", ctx(request, db))

@app.post("/admin/gallery/upload")
async def gallery_upload_post(request: Request, db: Session = Depends(get_db),
                               user: User = Depends(require_role("superadmin","media","ict")),
                               title: str=Form(...), category: str=Form(...),
                               image_url: str=Form(""), role: str=Form(""),
                               bio: str=Form(""), image: UploadFile=File(None)):
    url = save_upload(image) or image_url
    db.add(GalleryItem(title=title, category=category, url=url, role=role, bio=bio,
                       uploaded_by=user.name, date=datetime.utcnow().strftime("%Y-%m-%d")))
    db.commit()
    flash(request, "Photo uploaded successfully.")
    return RedirectResponse("/admin/gallery", 302)

@app.post("/admin/gallery/{gid}/delete")
def gallery_delete(gid: int, request: Request, db: Session = Depends(get_db),
                   user: User = Depends(require_role("superadmin","media","ict"))):
    g = db.get(GalleryItem, gid)
    if g: db.delete(g); db.commit()
    flash(request, "Photo removed.")
    return RedirectResponse("/admin/gallery", 302)

# ═══════════════════════════════════════════════════════════════
# CALENDAR
# ═══════════════════════════════════════════════════════════════

@app.get("/admin/calendar", response_class=HTMLResponse)
def calendar_list(request: Request, db: Session = Depends(get_db),
                  user: User = Depends(require_role("superadmin","ict"))):
    items = db.exec(select(CalendarEvent).order_by(CalendarEvent.date)).all()
    return templates.TemplateResponse("admin/calendar.html", ctx(request, db, items=items))

@app.get("/admin/calendar/create", response_class=HTMLResponse)
def calendar_create_page(request: Request, db: Session = Depends(get_db),
                         user: User = Depends(require_role("superadmin","ict"))):
    return templates.TemplateResponse("admin/calendar_form.html", ctx(request, db, item=None))

@app.post("/admin/calendar/create")
def calendar_create_post(request: Request, db: Session = Depends(get_db),
                         user: User = Depends(require_role("superadmin","ict")),
                         type: str=Form(...), title: str=Form(...),
                         date: str=Form(...), note: str=Form("")):
    db.add(CalendarEvent(type=type, title=title, date=date, note=note))
    db.commit()
    flash(request, "Calendar entry added.")
    return RedirectResponse("/admin/calendar", 302)

@app.post("/admin/calendar/{cid}/delete")
def calendar_delete(cid: int, request: Request, db: Session = Depends(get_db),
                    user: User = Depends(require_role("superadmin","ict"))):
    c = db.get(CalendarEvent, cid)
    if c: db.delete(c); db.commit()
    flash(request, "Entry removed.")
    return RedirectResponse("/admin/calendar", 302)

# ═══════════════════════════════════════════════════════════════
# SITE INFO
# ═══════════════════════════════════════════════════════════════

@app.get("/admin/siteinfo", response_class=HTMLResponse)
def siteinfo_page(request: Request, db: Session = Depends(get_db),
                  user: User = Depends(require_role("superadmin","ict"))):
    keys = ["phone1","phone2","email","address","tagline",
            "facebook","instagram","whatsapp","youtube",
            "nursery_count","jss_count","sss_count","teacher_count"]
    return templates.TemplateResponse("admin/siteinfo.html",
        ctx(request, db, data={k: get_info(db, k) for k in keys}))

@app.post("/admin/siteinfo")
def siteinfo_post(request: Request, db: Session = Depends(get_db),
                  user: User = Depends(require_role("superadmin","ict")),
                  phone1: str=Form(""), phone2: str=Form(""), email: str=Form(""),
                  address: str=Form(""), tagline: str=Form(""),
                  facebook: str=Form(""), instagram: str=Form(""),
                  whatsapp: str=Form(""), youtube: str=Form(""),
                  nursery_count: str=Form(""), jss_count: str=Form(""),
                  sss_count: str=Form(""), teacher_count: str=Form("")):
    for k, v in locals().items():
        if k not in ("request","db","user"): set_info(db, k, v)
    flash(request, "Site information saved and live on website.")
    return RedirectResponse("/admin/siteinfo", 302)

# ═══════════════════════════════════════════════════════════════
# ADD THESE ROUTES to main.py  (after the existing routes)
# ═══════════════════════════════════════════════════════════════


@app.get("/api/stats")
def api_stats(db: Session = Depends(get_db)):
    students   = db.exec(select(Student)).all()
    staff      = db.exec(select(StaffUser)).all()
    news_count = len(db.exec(select(News).where(News.published == True)).all())
    nursery  = get_info(db, "nursery_count",  str(len([s for s in students if "primary" in s.level.lower()])))
    jss      = get_info(db, "jss_count",      str(len([s for s in students if "jss" in s.level.lower()])))
    sss      = get_info(db, "sss_count",      str(len([s for s in students if "sss" in s.level.lower()])))
    teachers = get_info(db, "teacher_count",  str(len(staff)))
    return {
        "nursery_count":  nursery,
        "jss_count":      jss,
        "sss_count":      sss,
        "teacher_count":  teachers,
        "total_students": str(len(students)),
        "news_count":     str(news_count),
    }

# ── STAFF AUTH ────────────────────────────────────────────────

@app.get("/staff/login", response_class=HTMLResponse)
def staff_login_page(request: Request, db: Session = Depends(get_db)):
    school_logo = db.exec(select(Logo).where(Logo.logo_type == "school")).first()
    return templates.TemplateResponse("portals/staff_login.html",
        {"request": request, "school_logo": school_logo, "flash_msgs": get_flash(request)})

@app.post("/staff/login")
def staff_login_post(request: Request, db: Session = Depends(get_db),
                     email: str = Form(...), password: str = Form(...)):
    staff = db.exec(select(StaffUser).where(StaffUser.email == email)).first()
    if staff and staff.status == "active" and verify_password(password, staff.password):
        request.session["staff_id"] = staff.id
        request.session["staff_role"] = staff.role
        return RedirectResponse("/staff/dashboard", 302)
    flash(request, "Invalid credentials.", "error")
    return RedirectResponse("/staff/login", 302)

@app.get("/staff/logout")
def staff_logout(request: Request):
    request.session.pop("staff_id", None)
    request.session.pop("staff_role", None)
    return RedirectResponse("/staff/login", 302)

def get_staff(request: Request, db: Session = Depends(get_db)) -> StaffUser:
    sid = request.session.get("staff_id")
    if not sid:
        raise HTTPException(302, headers={"Location": "/staff/login"})
    s = db.exec(select(StaffUser).where(StaffUser.id == sid)).first()
    if not s or s.status != "active":
        raise HTTPException(302, headers={"Location": "/staff/login"})
    return s

def staff_ctx(request: Request, db: Session, **kw):
    school_logo = db.exec(select(Logo).where(Logo.logo_type == "school")).first()
    return {"request": request, "staff": get_staff(request, db),
            "school_logo": school_logo, "flash_msgs": get_flash(request), **kw}

# ── STAFF DASHBOARD ───────────────────────────────────────────

@app.get("/staff/dashboard", response_class=HTMLResponse)
def staff_dashboard(request: Request, db: Session = Depends(get_db)):
    s = get_staff(request, db)
    students = db.exec(select(Student).where(Student.class_name == s.class_name)).all()
    assignments = db.exec(select(Assignment).where(Assignment.teacher_id == s.id)).all()
    pending_subs = db.exec(select(AssignmentSubmission).where(
        AssignmentSubmission.status == "submitted")).all()
    school_logo = db.exec(select(Logo).where(Logo.logo_type == "school")).first()
    return templates.TemplateResponse("portals/staff_dashboard.html", {
        "request": request, "staff": s, "students": students,
        "assignments": assignments, "pending_subs": pending_subs,
        "school_logo": school_logo, "flash_msgs": get_flash(request)
    })

# ── STUDENTS (CRUD by staff/admin) ────────────────────────────

@app.get("/staff/students", response_class=HTMLResponse)
def staff_students(request: Request, db: Session = Depends(get_db)):
    s = get_staff(request, db)
    students = db.exec(select(Student).order_by(Student.class_name)).all()
    school_logo = db.exec(select(Logo).where(Logo.logo_type == "school")).first()
    return templates.TemplateResponse("portals/staff_students.html",
        {"request": request, "staff": s, "students": students,
         "school_logo": school_logo, "flash_msgs": get_flash(request)})

@app.post("/staff/students/add")
def staff_add_student(request: Request, db: Session = Depends(get_db),
                      full_name: str = Form(...), admission_no: str = Form(...),
                      class_name: str = Form(...), level: str = Form(...),
                      gender: str = Form(...), parent_email: str = Form(""),
                      parent_phone: str = Form(""), session: str = Form("2025/2026")):
    s = get_staff(request, db)
    if db.exec(select(Student).where(Student.admission_no == admission_no)).first():
        flash(request, "Admission number already exists.", "error")
    else:
        db.add(Student(full_name=full_name, admission_no=admission_no,
                       class_name=class_name, level=level, gender=gender,
                       parent_email=parent_email, parent_phone=parent_phone,
                       session=session, added_by=s.name))
        db.commit()
        flash(request, f"Student {full_name} added successfully.")
    return RedirectResponse("/staff/students", 302)

@app.post("/staff/students/{sid}/delete")
def staff_delete_student(sid: int, request: Request, db: Session = Depends(get_db)):
    get_staff(request, db)
    st = db.get(Student, sid)
    if st: db.delete(st); db.commit()
    flash(request, "Student removed.")
    return RedirectResponse("/staff/students", 302)

# ── ASSIGNMENTS ───────────────────────────────────────────────

@app.get("/staff/assignments", response_class=HTMLResponse)
def staff_assignments(request: Request, db: Session = Depends(get_db)):
    s = get_staff(request, db)
    items = db.exec(select(Assignment).where(Assignment.teacher_id == s.id).order_by(Assignment.id.desc())).all()
    school_logo = db.exec(select(Logo).where(Logo.logo_type == "school")).first()
    return templates.TemplateResponse("portals/staff_assignments.html",
        {"request": request, "staff": s, "items": items,
         "school_logo": school_logo, "flash_msgs": get_flash(request)})

@app.post("/staff/assignments/create")
def staff_create_assignment(request: Request, db: Session = Depends(get_db),
                             title: str = Form(...), description: str = Form(""),
                             subject: str = Form(...), class_name: str = Form(...),
                             due_date: str = Form(...), term: str = Form("Third Term"),
                             session: str = Form("2025/2026")):
    s = get_staff(request, db)
    db.add(Assignment(title=title, description=description, subject=subject,
                      class_name=class_name, due_date=due_date, term=term,
                      session=session, created_by=s.name, teacher_id=s.id))
    db.commit()
    flash(request, "Assignment created and published to students.")
    return RedirectResponse("/staff/assignments", 302)

@app.get("/staff/assignments/{aid}/submissions", response_class=HTMLResponse)
def staff_view_submissions(aid: int, request: Request, db: Session = Depends(get_db)):
    s = get_staff(request, db)
    asgn = db.get(Assignment, aid)
    subs = db.exec(select(AssignmentSubmission).where(
        AssignmentSubmission.assignment_id == aid)).all()
    school_logo = db.exec(select(Logo).where(Logo.logo_type == "school")).first()
    return templates.TemplateResponse("portals/staff_submissions.html",
        {"request": request, "staff": s, "assignment": asgn, "subs": subs,
         "school_logo": school_logo, "flash_msgs": get_flash(request)})

@app.post("/staff/submissions/{sub_id}/grade")
def staff_grade_submission(sub_id: int, request: Request, db: Session = Depends(get_db),
                           grade: str = Form(...), feedback: str = Form("")):
    get_staff(request, db)
    sub = db.get(AssignmentSubmission, sub_id)
    if sub:
        sub.grade = grade; sub.feedback = feedback; sub.status = "graded"
        db.add(sub); db.commit()
        flash(request, "Submission graded successfully.")
    return RedirectResponse(f"/staff/assignments/{sub.assignment_id}/submissions", 302)

# ── EXAM RESULTS ──────────────────────────────────────────────

@app.get("/staff/results", response_class=HTMLResponse)
def staff_results(request: Request, db: Session = Depends(get_db)):
    s = get_staff(request, db)
    results = db.exec(select(ExamResult).where(ExamResult.uploaded_by == s.name).order_by(ExamResult.id.desc())).all()
    students = db.exec(select(Student).order_by(Student.class_name)).all()
    school_logo = db.exec(select(Logo).where(Logo.logo_type == "school")).first()
    return templates.TemplateResponse("portals/staff_results.html",
        {"request": request, "staff": s, "results": results, "students": students,
         "school_logo": school_logo, "flash_msgs": get_flash(request)})

@app.post("/staff/results/upload")
def staff_upload_result(request: Request, db: Session = Depends(get_db),
                        student_id: int = Form(...), subject: str = Form(...),
                        ca1: float = Form(0), ca2: float = Form(0),
                        exam: float = Form(0), term: str = Form("Third Term"),
                        session: str = Form("2025/2026")):
    s = get_staff(request, db)
    st = db.get(Student, student_id)
    if not st:
        flash(request, "Student not found.", "error")
        return RedirectResponse("/staff/results", 302)
    total = ca1 + ca2 + exam
    grade = "A" if total >= 75 else "B" if total >= 65 else "C" if total >= 55 else "D" if total >= 45 else "F"
    remark = "Excellent" if total >= 75 else "Very Good" if total >= 65 else "Good" if total >= 55 else "Fair" if total >= 45 else "Fail"
    # check if result already exists for this student/subject/term/session
    existing = db.exec(select(ExamResult).where(
        ExamResult.student_id == student_id,
        ExamResult.subject == subject,
        ExamResult.term == term,
        ExamResult.session == session
    )).first()
    if existing:
        existing.ca1=ca1; existing.ca2=ca2; existing.exam=exam
        existing.total=total; existing.grade=grade; existing.remark=remark
        existing.approved=False; existing.uploaded_by=s.name
        db.add(existing)
    else:
        db.add(ExamResult(student_id=student_id, student_name=st.full_name,
                          admission_no=st.admission_no, class_name=st.class_name,
                          subject=subject, ca1=ca1, ca2=ca2, exam=exam,
                          total=total, grade=grade, remark=remark,
                          term=term, session=session, uploaded_by=s.name,
                          approved=False))
    db.commit()
    flash(request, f"Result for {st.full_name} uploaded. Awaiting Principal approval.")
    return RedirectResponse("/staff/results", 302)


# ── ADMIN PROFILE ─────────────────────────────────────────────────────────

@app.get("/admin/profile", response_class=HTMLResponse)
def admin_profile(request: Request, db: Session = Depends(get_db),
                  user: User = Depends(require_login)):
    return templates.TemplateResponse("admin/profile.html", ctx(request, db))

@app.post("/admin/profile")
async def admin_profile_post(request: Request, db: Session = Depends(get_db),
                              user: User = Depends(require_login),
                              name: str = Form(...),
                              current_password: str = Form(""),
                              new_password: str = Form(""),
                              avatar: UploadFile = File(None)):
    u = db.get(User, user.id)
    if not u:
        return RedirectResponse("/admin", 302)
    u.name = name
    if current_password and new_password:
        if verify_password(current_password, u.password):
            u.password = hash_password(new_password)
            flash(request, "Password updated successfully.")
        else:
            flash(request, "Current password is incorrect.", "error")
            return RedirectResponse("/admin/profile", 302)
    if avatar and avatar.filename:
        url = save_upload(avatar)
        if url: u.avatar = url
    db.add(u); db.commit()
    flash(request, "Profile updated successfully.")
    return RedirectResponse("/admin/profile", 302)

# ── STUDENT SEARCH API ─────────────────────────────────────────────────────

@app.get("/api/students/search")
def search_students(q: str = "", db: Session = Depends(get_db)):
    students = db.exec(select(Student)).all()
    if q:
        ql = q.lower()
        students = [s for s in students if ql in s.full_name.lower()
                    or ql in s.admission_no.lower()
                    or ql in s.class_name.lower()]
    return [{"id": s.id, "name": s.full_name, "class_name": s.class_name,
             "admission_no": s.admission_no, "level": s.level} for s in students[:20]]

# ── PARENT EDIT ROUTE ──────────────────────────────────────────────────────

@app.post("/admin/parents/{pid}/edit")
def admin_edit_parent(pid: int, request: Request, db: Session = Depends(get_db),
                      user: User = Depends(require_role("superadmin","ict")),
                      name: str = Form(...), email: str = Form(...),
                      password: str = Form(""), phone: str = Form(""),
                      student_ids: str = Form("")):
    p = db.get(ParentUser, pid)
    if p:
        p.name = name; p.email = email; p.phone = phone; p.student_ids = student_ids
        if password.strip(): p.password = hash_password(password)
        db.add(p); db.commit()
        flash(request, f"Parent account for {name} updated.")
    return RedirectResponse("/admin/parents", 302)

# ── STAFF TOGGLE ───────────────────────────────────────────────────────────

@app.post("/admin/staff/{sid}/toggle")
def admin_toggle_staff(sid: int, request: Request, db: Session = Depends(get_db),
                       user: User = Depends(require_role("superadmin","ict"))):
    s = db.get(StaffUser, sid)
    if s:
        s.status = "inactive" if s.status == "active" else "active"
        db.add(s); db.commit()
        flash(request, f"Staff status updated to {s.status}.")
    return RedirectResponse("/admin/staff", 302)

# ── PRINTABLE RESULT SHEET ─────────────────────────────────────────────────

@app.get("/parent/results/{student_id}/print", response_class=HTMLResponse)
def print_results(student_id: int, request: Request, db: Session = Depends(get_db),
                  term: str = "Third Term", session: str = "2025/2026"):
    p = get_parent(request, db)
    ids = [int(i) for i in p.student_ids.split(",") if i.strip().isdigit()]
    if student_id not in ids:
        raise HTTPException(403, detail="Access denied")
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(404)
    results = db.exec(select(ExamResult).where(
        ExamResult.student_id == student_id,
        ExamResult.approved == True,
        ExamResult.term == term,
        ExamResult.session == session
    )).all()
    school_logo = db.exec(select(Logo).where(Logo.logo_type == "school")).first()
    site = {k: get_info(db, k) for k in ["phone1","phone2","email","address","tagline"]}
    return templates.TemplateResponse("portals/result_sheet.html",
        {"request": request, "student": student, "results": results,
         "term": term, "session": session, "parent": p,
         "school_logo": school_logo, "site": site})


# ── ADMIN: APPROVE RESULTS + MANAGE STAFF ─────────────────────

@app.get("/admin/results", response_class=HTMLResponse)
def admin_results(request: Request, db: Session = Depends(get_db),
                  user: User = Depends(require_role("superadmin","ict"))):
    pending = db.exec(select(ExamResult).where(ExamResult.approved == False)).all()
    approved = db.exec(select(ExamResult).where(ExamResult.approved == True).order_by(ExamResult.id.desc()).limit(50)).all()
    return templates.TemplateResponse("admin/results.html",
        ctx(request, db, pending=pending, approved=approved))

@app.post("/admin/results/{rid}/approve")
def admin_approve_result(rid: int, request: Request, db: Session = Depends(get_db),
                         user: User = Depends(require_role("superadmin","ict"))):
    r = db.get(ExamResult, rid)
    if r: r.approved = True; db.add(r); db.commit()
    flash(request, "Result approved and now visible to parents.")
    return RedirectResponse("/admin/results", 302)

@app.post("/admin/results/{rid}/approve-all")
def admin_approve_all(request: Request, db: Session = Depends(get_db),
                      user: User = Depends(require_role("superadmin"))):
    pending = db.exec(select(ExamResult).where(ExamResult.approved == False)).all()
    for r in pending:
        r.approved = True; db.add(r)
    db.commit()
    flash(request, f"All {len(pending)} pending results approved.")
    return RedirectResponse("/admin/results", 302)

@app.get("/admin/staff", response_class=HTMLResponse)
def admin_staff_list(request: Request, db: Session = Depends(get_db),
                     user: User = Depends(require_role("superadmin"))):
    staff = db.exec(select(StaffUser).order_by(StaffUser.name)).all()
    return templates.TemplateResponse("admin/staff_list.html", ctx(request, db, staff=staff))

@app.post("/admin/staff/create")
def admin_create_staff(request: Request, db: Session = Depends(get_db),
                       user: User = Depends(require_role("superadmin")),
                       name: str = Form(...), email: str = Form(...),
                       password: str = Form(...), role: str = Form("teacher"),
                       subject: str = Form(""), class_name: str = Form(""),
                       section: str = Form("")):
    if db.exec(select(StaffUser).where(StaffUser.email == email)).first():
        flash(request, "Email already exists.", "error")
    else:
        db.add(StaffUser(name=name, email=email, password=hash_password(password),
                         role=role, subject=subject, class_name=class_name, section=section))
        db.commit()
        flash(request, f"Staff account created for {name}.")
    return RedirectResponse("/admin/staff", 302)

@app.post("/admin/staff/{sid}/delete")
def admin_delete_staff(sid: int, request: Request, db: Session = Depends(get_db),
                       user: User = Depends(require_role("superadmin"))):
    s = db.get(StaffUser, sid)
    if s: db.delete(s); db.commit()
    flash(request, "Staff account deleted.")
    return RedirectResponse("/admin/staff", 302)

# ── PARENT AUTH ───────────────────────────────────────────────

@app.get("/parent/login", response_class=HTMLResponse)
def parent_login_page(request: Request, db: Session = Depends(get_db)):
    school_logo = db.exec(select(Logo).where(Logo.logo_type == "school")).first()
    return templates.TemplateResponse("portals/parent_login.html",
        {"request": request, "school_logo": school_logo, "flash_msgs": get_flash(request)})

@app.post("/parent/login")
def parent_login_post(request: Request, db: Session = Depends(get_db),
                      email: str = Form(...), password: str = Form(...)):
    p = db.exec(select(ParentUser).where(ParentUser.email == email)).first()
    if p and p.status == "active" and verify_password(password, p.password):
        request.session["parent_id"] = p.id
        return RedirectResponse("/parent/dashboard", 302)
    flash(request, "Invalid credentials.", "error")
    return RedirectResponse("/parent/login", 302)

@app.get("/parent/logout")
def parent_logout(request: Request):
    request.session.pop("parent_id", None)
    return RedirectResponse("/parent/login", 302)

def get_parent(request: Request, db: Session = Depends(get_db)) -> ParentUser:
    pid = request.session.get("parent_id")
    if not pid:
        raise HTTPException(302, headers={"Location": "/parent/login"})
    p = db.exec(select(ParentUser).where(ParentUser.id == pid)).first()
    if not p or p.status != "active":
        raise HTTPException(302, headers={"Location": "/parent/login"})
    return p

@app.get("/parent/dashboard", response_class=HTMLResponse)
def parent_dashboard(request: Request, db: Session = Depends(get_db)):
    p = get_parent(request, db)
    ids = [int(i) for i in p.student_ids.split(",") if i.strip().isdigit()]
    students = [db.get(Student, i) for i in ids if db.get(Student, i)]
    results = {}
    assignments = {}
    for st in students:
        results[st.id] = db.exec(select(ExamResult).where(
            ExamResult.student_id == st.id, ExamResult.approved == True)).all()
        subs = db.exec(select(AssignmentSubmission).where(
            AssignmentSubmission.student_id == st.id)).all()
        assignments[st.id] = subs
    school_logo = db.exec(select(Logo).where(Logo.logo_type == "school")).first()
    return templates.TemplateResponse("portals/parent_dashboard.html",
        {"request": request, "parent": p, "students": students,
         "results": results, "assignments": assignments,
         "school_logo": school_logo, "flash_msgs": get_flash(request)})

# ── STUDENT AUTH ──────────────────────────────────────────────

@app.get("/student/login", response_class=HTMLResponse)
def student_login_page(request: Request, db: Session = Depends(get_db)):
    school_logo = db.exec(select(Logo).where(Logo.logo_type == "school")).first()
    return templates.TemplateResponse("portals/student_login.html",
        {"request": request, "school_logo": school_logo, "flash_msgs": get_flash(request)})

@app.post("/student/login")
def student_login_post(request: Request, db: Session = Depends(get_db),
                       admission_no: str = Form(...), password: str = Form(...)):
    # password is admission number by default (school can change)
    st = db.exec(select(Student).where(Student.admission_no == admission_no)).first()
    if st and password == admission_no:   # default: admission no = password
        request.session["student_id"] = st.id
        return RedirectResponse("/student/dashboard", 302)
    flash(request, "Invalid admission number or password.", "error")
    return RedirectResponse("/student/login", 302)

@app.get("/student/logout")
def student_logout(request: Request):
    request.session.pop("student_id", None)
    return RedirectResponse("/student/login", 302)

def get_student_portal(request: Request, db: Session = Depends(get_db)) -> Student:
    sid = request.session.get("student_id")
    if not sid:
        raise HTTPException(302, headers={"Location": "/student/login"})
    st = db.get(Student, sid)
    if not st:
        raise HTTPException(302, headers={"Location": "/student/login"})
    return st

@app.get("/student/dashboard", response_class=HTMLResponse)
def student_dashboard(request: Request, db: Session = Depends(get_db)):
    st = get_student_portal(request, db)
    assignments = db.exec(select(Assignment).where(
        Assignment.class_name == st.class_name).order_by(Assignment.id.desc())).all()
    my_subs = {s.assignment_id: s for s in db.exec(select(AssignmentSubmission).where(
        AssignmentSubmission.student_id == st.id)).all()}
    results = db.exec(select(ExamResult).where(
        ExamResult.student_id == st.id, ExamResult.approved == True)).all()
    school_logo = db.exec(select(Logo).where(Logo.logo_type == "school")).first()
    return templates.TemplateResponse("portals/student_dashboard.html",
        {"request": request, "student": st, "assignments": assignments,
         "my_subs": my_subs, "results": results,
         "school_logo": school_logo, "flash_msgs": get_flash(request)})

@app.post("/student/assignments/{aid}/submit")
async def student_submit_assignment(aid: int, request: Request,
                                    db: Session = Depends(get_db),
                                    content: str = Form(""),
                                    file: UploadFile = File(None)):
    st = get_student_portal(request, db)
    existing = db.exec(select(AssignmentSubmission).where(
        AssignmentSubmission.assignment_id == aid,
        AssignmentSubmission.student_id == st.id)).first()
    file_url = save_upload(file) if file and file.filename else ""
    if existing:
        existing.content = content; existing.file_url = file_url
        existing.status = "submitted"; existing.submitted_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
        db.add(existing)
    else:
        db.add(AssignmentSubmission(assignment_id=aid, student_id=st.id,
                                    student_name=st.full_name, content=content,
                                    file_url=file_url, status="submitted"))
    db.commit()
    flash(request, "Assignment submitted successfully!")
    return RedirectResponse("/student/dashboard", 302)

# ── ADMIN: PARENT ACCOUNT MANAGEMENT ─────────────────────────

@app.get("/admin/parents", response_class=HTMLResponse)
def admin_parents(request: Request, db: Session = Depends(get_db),
                  user: User = Depends(require_role("superadmin"))):
    parents = db.exec(select(ParentUser).order_by(ParentUser.name)).all()
    students = db.exec(select(Student).order_by(Student.full_name)).all()
    return templates.TemplateResponse("admin/parents.html",
        ctx(request, db, parents=parents, students=students))

@app.post("/admin/parents/create")
def admin_create_parent(request: Request, db: Session = Depends(get_db),
                        user: User = Depends(require_role("superadmin")),
                        name: str = Form(...), email: str = Form(...),
                        password: str = Form(...), phone: str = Form(""),
                        student_ids: str = Form("")):
    if db.exec(select(ParentUser).where(ParentUser.email == email)).first():
        flash(request, "Email already exists.", "error")
    else:
        db.add(ParentUser(name=name, email=email, password=hash_password(password),
                          phone=phone, student_ids=student_ids))
        db.commit()
        flash(request, f"Parent account created for {name}.")
    return RedirectResponse("/admin/parents", 302)

@app.post("/admin/parents/{pid}/edit")
def admin_edit_parent(pid: int, request: Request, db: Session = Depends(get_db),
                      user: User = Depends(require_role("superadmin")),
                      name: str = Form(...), email: str = Form(...),
                      password: str = Form(""), phone: str = Form(""),
                      student_ids: str = Form("")):
    p = db.get(ParentUser, pid)
    if p:
        p.name = name
        p.email = email
        p.phone = phone
        p.student_ids = student_ids
        if password.strip():
            p.password = hash_password(password)
        db.add(p)
        db.commit()
        flash(request, f"Parent account for {name} updated successfully.")
    return RedirectResponse("/admin/parents", 302)

@app.post("/admin/parents/{pid}/delete")
def admin_delete_parent(pid: int, request: Request, db: Session = Depends(get_db),
                        user: User = Depends(require_role("superadmin"))):
    p = db.get(ParentUser, pid)
    if p: db.delete(p); db.commit()
    flash(request, "Parent account deleted.")
    return RedirectResponse("/admin/parents", 302)