# interlink-backend — Django REST API

## Stack

- **Python** 3.10+
- **Django** 5.0.3
- **Django REST Framework** 3.14
- **Auth**: `djangorestframework-simplejwt` (60 min access, 7 day refresh)
- **Database**: SQLite3 (dev) / PostgreSQL (prod via env vars)
- **Docs**: `drf-spectacular` — Swagger at `/swagger/`, ReDoc at `/redoc/`
- **Admin UI**: Django admin with Jazzmin theme at `/admin/`
- **Storage**: Local `/media/` by default; AWS S3 via env vars

## Running

```bash
source venv/bin/activate
python manage.py runserver          # http://127.0.0.1:8000
python manage.py migrate
python manage.py seed_all           # populate sample data
python manage.py createsuperuser    # create admin account
```

## Django apps

| App | URL prefix | Purpose |
|---|---|---|
| `accounts` | `/api/auth/` | JWT login/register, profile, password reset |
| `courses` | `/api/courses/` | Courses, modules, lessons, enrollment, reviews, certificates |
| `content` | `/api/content/` | About, team, blog, gallery, testimonials, FAQs, policies, homepage |
| `resources` | `/api/resources/` | Downloadable materials, ratings, bookmarks, collections |
| `contact` | `/api/contact/` | Contact form (placeholder, not yet fully implemented) |
| `enrollment` | — | Placeholder; core enrollment logic lives in `courses` |
| `seeder` | — | `manage.py seed_*` commands for local dev data |

## Key models per app

**accounts**: `UserProfile` (role: student/instructor/staff/admin), `PasswordResetToken`

**courses**: `Course` (slug PK for detail endpoints), `CourseCategory`, `CourseModule`,
`CourseLesson`, `Enrollment` (tracks progress %), `CourseReview`, `Certificate`

**content**: `AboutPage` (singleton), `TeamMember`, `BlogPost`, `BlogCategory`,
`GalleryItem`, `GalleryCategory`, `Testimonial`, `Policy`, `PolicyCategory`,
`FAQ`, `Partner`, `Achievement`, `HomepageSettings` (singleton)

**resources**: `Resource` (types: pdf/doc/xlsx/pptx/image/video/audio/link),
`ResourceCategory`, `ResourceRating`, `ResourceDownload`, `ResourceView`,
`ResourceCollection`, `StudyGuide`, `UserBookmark`

## Default permission

`IsAuthenticatedOrReadOnly` — unauthenticated GET requests are allowed everywhere.
Write operations require a valid JWT. Admin-level operations check `is_staff` or role.

## API conventions

- List endpoints return paginated JSON: `{ count, next, previous, results }`
- Detail endpoints for courses use **slug** (`/api/courses/<slug>/`)
- Detail endpoints for most content use **integer ID** (`/api/content/team/<id>/`)
- Singleton endpoints (`/api/content/about/`, `/api/content/homepage/`) use GET + PATCH

## Seeder commands

```bash
python manage.py seed_all          # run all seeders
python manage.py seed_courses
python manage.py seed_resources
python manage.py seed_content
python manage.py seed_team
python manage.py seed_gallery
python manage.py seed_blog
python manage.py seed_testimonials
python manage.py seed_policies
python manage.py seed_users
```

## Environment variables (`.env`)

```
SECRET_KEY=
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME= DB_USER= DB_PASSWORD= DB_HOST= DB_PORT=  # PostgreSQL (leave blank for SQLite)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
FRONTEND_URL=http://localhost:5173
JWT_ACCESS_TOKEN_LIFETIME=60        # minutes
JWT_REFRESH_TOKEN_LIFETIME=10080    # minutes (7 days)
AWS_ACCESS_KEY_ID=                  # optional S3 storage
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
```

## CORS

Allowed origins in `settings.py`: `http://localhost:3000`, `http://localhost:5173`.
Add `http://localhost:5174` and your production domain before deploying.

## Testing (not yet implemented)

No test suite exists. Use `pytest-django` when adding tests.
Place test files in `<app>/tests/` following Django conventions.
