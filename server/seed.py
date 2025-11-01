import os
from datetime import datetime, date
from app.models import db, User, Cohort, Project, ProjectMember, ActivityLog, Task, Class
from run import create_app
from sqlalchemy import text

# -----------------------------
# Load environment variables for passwords
# -----------------------------
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "adminpass")
STUDENT_PASSWORD = os.environ.get("STUDENT_PASSWORD", "studentpass")

# -----------------------------
# Initialize app context
# -----------------------------
app = create_app()

with app.app_context():
    # -----------------------------
    # Truncate tables & reset identities
    # -----------------------------
    print("⚠️ Truncating all tables...")
    db.session.execute(
        text('TRUNCATE TABLE users, cohorts, classes, projects, project_members, tasks, activity_logs RESTART IDENTITY CASCADE')
    )
    db.session.commit()

    # -----------------------------
    # Seed Classes
    # -----------------------------
    print("⚡ Seeding classes...")
    classes = [
        Class(name="Fullstack Web", description="Fullstack development track"),
        Class(name="Android Development", description="Mobile development track"),
        Class(name="Data Science", description="Data Science and analytics track"),
        Class(name="DevOps Track", description="DevOps and infrastructure track"),
        Class(name="Product Design", description="UI/UX and product design track"),
        Class(name="Cyber Security", description="Security and ethical hacking track"),
    ]
    db.session.add_all(classes)
    db.session.commit()
    print(f"✅ Classes seeded: {len(classes)} classes")

    # -----------------------------
    # Seed Users
    # -----------------------------
    print("⚡ Seeding users...")
    admin = User(
        name="Admin User",
        email="admin@test.com",
        role="Admin"
    )
    admin.set_password(ADMIN_PASSWORD)

    students = []
    for i in range(1, 6):
        student = User(
            name=f"Student {i}",
            email=f"student{i}@example.com",
            role="Student"
        )
        student.set_password(STUDENT_PASSWORD)

        # Assign a class deterministically
        student.class_id = classes[i % len(classes)].id

        students.append(student)

    db.session.add(admin)
    db.session.add_all(students)
    db.session.commit()
    print("✅ Users seeded: 1 Admin + 5 Students")

    # -----------------------------
    # Seed additional test users for pytest
    # -----------------------------
    test_users = [
        {"name": "Owner Test", "email": "owner@test.com", "role": "Student", "password": "pass", "class": classes[0]},
        {"name": "User1 Test", "email": "user1@test.com", "role": "Student", "password": "studentpass", "class": classes[1]},
        {"name": "Student Test", "email": "student@test.com", "role": "Student", "password": "studentpass", "class": classes[2]},
    ]

    for u in test_users:
        user = User(name=u["name"], email=u["email"], role=u["role"])
        user.set_password(u["password"])
        user.class_id = u["class"].id
        db.session.add(user)
    db.session.commit()
    print("✅ Test users seeded for pytest")

    # -----------------------------
    # Seed Cohorts
    # -----------------------------
    print("⚡ Seeding cohorts...")
    cohorts = [
        Cohort(
            name="Cohort Alpha",
            description="First cohort of 2025",
            start_date=date(2025, 1, 15),
            end_date=date(2025, 6, 30)
        ),
        Cohort(
            name="Cohort Beta",
            description="Second cohort of 2025",
            start_date=date(2025, 7, 1),
            end_date=date(2025, 12, 15)
        )
    ]
    db.session.add_all(cohorts)
    db.session.commit()
    print("✅ Cohorts seeded: 2 cohorts")

    # Assign students to cohorts deterministically
    for i, student in enumerate(students):
        student.cohort_id = cohorts[i % len(cohorts)].id
    db.session.commit()
    print("✅ Students assigned to cohorts")

    # -----------------------------
    # Seed Projects
    # -----------------------------
    print("⚡ Seeding projects...")
    project_templates = [
        {"name": "Project X", "description": "Fullstack web app", "track": "Fullstack"},
        {"name": "Project Y", "description": "Data analysis project", "track": "Data Science"},
        {"name": "Project Z", "description": "Mobile app", "track": "Mobile"},
    ]

    tags_by_track = {
        "Fullstack": ["Python", "Flask", "React", "PostgreSQL"],
        "Data Science": ["Python", "Pandas", "NumPy", "Machine Learning"],
        "Mobile": ["Android", "Java", "Kotlin", "Flutter"]
    }

    statuses = ["In Progress", "Completed", "Under Review"]
    projects = []

    for i, template in enumerate(project_templates):
        owner = students[i % len(students)]
        project = Project(
            name=template["name"],
            description=template["description"],
            owner_id=owner.id,
            class_id=owner.class_id,  # Assign same class as the owner
            cohort_id=owner.cohort_id,  # Assign same cohort as the owner
            github_link=f"https://github.com/{owner.email.split('@')[0]}/{template['name'].replace(' ', '').lower()}",
            tags=",".join(tags_by_track[template["track"]][:2]),
            status=statuses[i % len(statuses)]
        )
        projects.append(project)

    db.session.add_all(projects)
    db.session.commit()
    print(f"✅ Projects seeded: {len(projects)} projects")

    # -----------------------------
    # Seed Project Members + Activity Logs
    # -----------------------------
    print("⚡ Seeding project members & activity logs...")
    for project in projects:
        possible_members = [s for s in students if s.id != project.owner_id]
        members_to_add = possible_members[:2]
        for member in members_to_add:
            db.session.add(ProjectMember(project_id=project.id, user_id=member.id, status="accepted"))
            db.session.add(ActivityLog(user_id=member.id, action=f"Joined project {project.name}"))

        db.session.add(ActivityLog(user_id=project.owner_id, action=f"Created project {project.name}"))

        if project.status == "Completed":
            db.session.add(ActivityLog(user_id=project.owner_id, action=f"Marked project {project.name} as Completed"))

    db.session.commit()
    print("✅ Project members & activity logs seeded")

    # -----------------------------
    # Seed Tasks for each Project
    # -----------------------------
    print("⚡ Seeding tasks...")
    task_templates = [
        "Setup project repository",
        "Design database schema",
        "Implement authentication",
        "Build REST API endpoints",
        "Connect frontend with backend",
        "Write unit tests",
        "Prepare documentation"
    ]

    task_statuses = ["To Do", "In Progress", "Completed"]

    for project in projects:
        for i in range(3):
            task = Task(
                title=task_templates[i],
                description=f"Task {i+1} for {project.name}",
                status=task_statuses[i % len(task_statuses)],
                project_id=project.id,
                assignee_id=students[i % len(students)].id,
                created_at=datetime.utcnow()
            )
            db.session.add(task)

        db.session.add(ActivityLog(user_id=project.owner_id, action=f"Created 3 tasks for {project.name}"))

    db.session.commit()
    print(" Tasks seeded for each project")

    # -----------------------------
    # Seed Admin Activity Logs
    # -----------------------------
    admin_logs = [
        ActivityLog(user_id=admin.id, action="Seeded database with admin, students, and tasks"),
        ActivityLog(user_id=admin.id, action="Reviewed all project submissions")
    ]
    db.session.add_all(admin_logs)
    db.session.commit()

    print(" Database seeded successfully! 2FA is disabled by default. Users can enable it after login.")
