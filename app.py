from flask import Flask, request, redirect, url_for, render_template_string, session
import sqlite3
import uuid
from datetime import datetime

app = Flask(__name__)

app.secret_key = "neon_arena_demo_secret_change_me"

ADMIN_PASSWORD = "admin123"
DATABASE = "tournament.db"


TOURNAMENTS = [
    {"name": "BGMI Solo Clash", "fee": 50, "date": "Coming Soon"},
    {"name": "Free Fire Solo War", "fee": 30, "date": "Coming Soon"},
    {"name": "BGMI Squad Championship", "fee": 100, "date": "Coming Soon"},
]


# =========================================================
# CSS
# =========================================================

CSS = """
<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    min-height: 100vh;
    font-family: Arial, sans-serif;
    color: white;

    background:
        radial-gradient(circle at 10% 10%, #7c3aed88, transparent 32%),
        radial-gradient(circle at 90% 90%, #00e5ff66, transparent 32%),
        linear-gradient(135deg, #04000f, #08001b, #00131c);
}

.container {
    width: 92%;
    max-width: 850px;
    margin: auto;
    padding: 28px 0 50px;
}

.logo {
    text-align: center;
    font-size: clamp(36px, 9vw, 58px);
    font-weight: 900;

    background:
        linear-gradient(90deg, #00f7ff, #7c3aed, #ff00c8);

    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}

.subtitle {
    text-align: center;
    color: #aab4c5;
    margin: 8px 0 25px;
}

.card {
    margin-top: 20px;
    padding: 22px;
    border-radius: 22px;

    background: #090923cc;

    border: 1px solid #00f7ff3d;

    box-shadow:
        0 0 28px #00f7ff14;

    backdrop-filter: blur(10px);
}

h2 {
    color: #00f7ff;
    margin-top: 0;
}

.tournament {
    padding: 17px;
    margin-top: 12px;
    border-radius: 15px;

    background: #ffffff09;

    border: 1px solid #29334d;
}

.tournament:hover {
    border-color: #00f7ff;
}

.name {
    font-size: 18px;
    font-weight: bold;
}

.fee {
    color: #ff4fd8;
    font-weight: bold;
    margin-top: 8px;
}

.date,
.small {
    color: #94a3b8;
    font-size: 14px;
}

label {
    display: block;
    margin: 16px 0 7px;
    color: #dbeafe;
    font-weight: bold;
}

input,
select {
    width: 100%;
    padding: 14px;

    border-radius: 12px;
    border: 1px solid #29354e;

    outline: 0;

    background: #070a1b;
    color: white;

    font-size: 15px;
}

input:focus,
select:focus {
    border-color: #00f7ff;

    box-shadow:
        0 0 12px #00f7ff2e;
}

button,
.btn {
    display: block;
    width: 100%;

    padding: 15px;
    margin-top: 18px;

    border: 0;
    border-radius: 14px;

    color: white;

    text-align: center;
    text-decoration: none;

    font-size: 16px;
    font-weight: bold;

    cursor: pointer;

    background:
        linear-gradient(
            90deg,
            #00c6ff,
            #7c3aed,
            #ff00c8
        );

    box-shadow:
        0 0 22px #00c6ff33;
}

.secondary {
    display: block;
    width: 100%;

    padding: 13px;
    margin-top: 12px;

    border: 1px solid #00e5ff;
    border-radius: 14px;

    color: #00e5ff;

    text-align: center;
    text-decoration: none;
    font-weight: bold;

    background: #00e5ff08;
}

.payment {
    margin-top: 22px;
    padding: 20px;

    text-align: center;

    border-radius: 18px;

    background: #00f7ff08;

    border: 1px solid #00f7ff4d;
}

.qr {
    width: 200px;
    height: 200px;

    margin: 15px auto;
    padding: 12px;

    background: white;
    color: black;

    border-radius: 14px;

    display: flex;
    align-items: center;
    justify-content: center;
}

.qr-inner {
    width: 100%;
    height: 100%;

    border: 3px dashed black;

    display: flex;
    align-items: center;
    justify-content: center;

    text-align: center;

    font-size: 21px;
    font-weight: 900;
}

.warning {
    color: #ffd166;
    font-size: 13px;
    line-height: 1.5;
}

.notice {
    margin-top: 16px;
    padding: 14px;

    border-radius: 12px;

    background: #ffffff08;

    color: #cbd5e1;

    line-height: 1.55;
    font-size: 14px;
}

.status {
    display: inline-block;

    padding: 9px 15px;

    border-radius: 50px;

    font-weight: bold;

    margin-top: 15px;
}

.pending {
    color: #ffd166;
    background: #ffd1661a;
}

.approved {
    color: #00ff9d;
    background: #00ff9d1a;
}

.rejected {
    color: #ff6680;
    background: #ff66801a;
}

.idbox {
    margin: 18px 0;
    padding: 15px;

    border-radius: 14px;

    border: 1px solid #00f7ff;

    color: #00f7ff;

    text-align: center;

    font-size: 24px;
    font-weight: 900;

    word-break: break-word;
}

.error {
    margin-top: 15px;
    padding: 12px;

    border-radius: 10px;

    color: #ff7188;

    background: #ff003c14;
}

.admin-item {
    padding: 18px;
    margin-top: 15px;

    border-radius: 17px;

    background: #ffffff08;

    border: 1px solid #29354e;
}

.admin-item.pending-border {
    border-color: #ffd166;
}

.admin-item.approved-border {
    border-color: #00ff9d;
}

.admin-item.rejected-border {
    border-color: #ff6680;
}

.data {
    color: #cbd5e1;

    line-height: 1.8;

    word-break: break-word;
}

.approve {
    background: #059669;
}

.reject {
    background: #dc2626;
}

.footer {
    text-align: center;

    margin-top: 28px;

    color: #64748b;

    font-size: 13px;
}

@media (max-width: 500px) {

    .container {
        width: 94%;
    }

    .card {
        padding: 18px;
    }

}

</style>
"""


# =========================================================
# PAGE TEMPLATE
# =========================================================

def page(title, body):

    return f"""
<!doctype html>

<html>

<head>

<meta name="viewport"
      content="width=device-width, initial-scale=1">

<title>{title}</title>

{CSS}

</head>

<body>

<div class="container">

<div class="logo">
    ⚡ NEON ARENA
</div>

<div class="subtitle">
    Gaming Tournament Registration
</div>

{body}

<div class="footer">
    ⚡ Neon Arena • Local Tournament Demo
</div>

</div>

</body>

</html>
"""


# =========================================================
# DATABASE
# =========================================================

def db():

    con = sqlite3.connect(DATABASE)

    con.row_factory = sqlite3.Row

    return con


def init_db():

    con = db()

    con.execute("""
        CREATE TABLE IF NOT EXISTS registrations (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            registration_id TEXT UNIQUE NOT NULL,

            tournament TEXT NOT NULL,

            player_name TEXT NOT NULL,

            player_uid TEXT NOT NULL,

            phone TEXT NOT NULL,

            transaction_id TEXT NOT NULL,

            entry_fee INTEGER NOT NULL,

            status TEXT NOT NULL DEFAULT 'PENDING',

            created_at TEXT NOT NULL

        )
    """)

    con.commit()

    con.close()


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    body = """

<div class="card">

<h2>
    🏆 Available Tournaments
</h2>

{% for t in tournaments %}

<div class="tournament">

<div class="name">
    {{ t.name }}
</div>

<div class="date">
    📅 {{ t.date }}
</div>

<div class="fee">
    💰 Entry Fee: ₹{{ t.fee }}
</div>

</div>

{% endfor %}

</div>


<div class="card">

<h2>
    🎮 Ready to Register?
</h2>

<p class="small">
    Fill your player details and submit
    a demo tournament registration.
</p>

<a class="btn" href="/register">
    🚀 REGISTER NOW
</a>

<a class="secondary" href="/status">
    🔎 CHECK MY REGISTRATION
</a>

<a class="secondary" href="/admin/login">
    🔐 ADMIN PANEL
</a>

</div>

"""

    return render_template_string(

        page("Neon Arena", body),

        tournaments=TOURNAMENTS

    )


# =========================================================
# REGISTER
# =========================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "GET":

        body = """

<div class="card">

<h2>
    📝 Player Details
</h2>

<form method="post">


<label>
    🏆 Select Tournament
</label>

<select
    name="tournament"
    required
>

<option value="">
    Select tournament
</option>

{% for t in tournaments %}

<option value="{{ t.name }}">

    {{ t.name }} — ₹{{ t.fee }}

</option>

{% endfor %}

</select>


<label>
    👤 Player Name
</label>

<input
    name="player_name"
    maxlength="60"
    placeholder="Enter player name"
    required
>


<label>
    🎮 Game UID / Player ID
</label>

<input
    name="player_uid"
    maxlength="60"
    placeholder="Enter game UID"
    required
>


<label>
    📱 Contact Number
</label>

<input
    name="phone"
    maxlength="20"
    placeholder="Enter contact number"
    required
>


<div class="payment">

<h3>
    💳 TEST PAYMENT SECTION
</h3>

<p>
    Demo QR is shown only so you can
    test the complete flow.
</p>


<div class="qr">

<div class="qr-inner">

    TEST QR

    <br>

    DEMO ONLY

</div>

</div>


<div class="warning">

⚠️ DEMO ONLY —
no real payment is processed here.

</div>

</div>


<label>
    🧾 Transaction / Reference ID
</label>

<input
    name="transaction_id"
    maxlength="100"
    placeholder="Example: TEST123456"
    required
>


<div class="notice">

Your registration is saved locally
and starts as <b>PENDING</b>.

Keep your Registration ID after submitting.

</div>


<button type="submit">

    🚀 SUBMIT REGISTRATION

</button>

</form>


<a class="secondary" href="/">

    ← Back to Home

</a>

</div>

"""

        return render_template_string(

            page("Register", body),

            tournaments=TOURNAMENTS

        )


    tournament = request.form.get(
        "tournament",
        ""
    ).strip()


    player_name = request.form.get(
        "player_name",
        ""
    ).strip()


    player_uid = request.form.get(
        "player_uid",
        ""
    ).strip()


    phone = request.form.get(
        "phone",
        ""
    ).strip()


    transaction_id = request.form.get(
        "transaction_id",
        ""
    ).strip()


    selected = next(

        (
            t for t in TOURNAMENTS
            if t["name"] == tournament
        ),

        None

    )


    if not selected:

        return "Invalid tournament.", 400


    if not all(
        [
            player_name,
            player_uid,
            phone,
            transaction_id
        ]
    ):

        return "Please fill all fields.", 400


    registration_id = (

        "NA-" +
        uuid.uuid4().hex[:8].upper()

    )


    con = db()


    con.execute(
        """

        INSERT INTO registrations

        (
            registration_id,
            tournament,
            player_name,
            player_uid,
            phone,
            transaction_id,
            entry_fee,
            status,
            created_at
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)

        """,

        (

            registration_id,

            tournament,

            player_name,

            player_uid,

            phone,

            transaction_id,

            selected["fee"],

            "PENDING",

            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        )

    )


    con.commit()

    con.close()


    body = f"""

<div class="card">

<h2>
    ✅ Registration Saved!
</h2>

<p>
    Your registration has been
    successfully stored.
</p>


<div class="small">
    Registration ID
</div>


<div class="idbox">

    {registration_id}

</div>


<div class="status pending">

    🟡 PENDING VERIFICATION

</div>


<div class="notice">

Save this Registration ID.

You can use it later to check your status.

</div>


<a class="btn"
   href="/status?rid={registration_id}">

    🔎 VIEW MY REGISTRATION

</a>


<a class="secondary"
   href="/">

    🏠 HOME

</a>

</div>

"""


    return page(
        "Registration Saved",
        body
    )


# =========================================================
# STATUS
# =========================================================

@app.route("/status")
def status():

    rid = request.args.get(
        "rid",
        ""
    ).strip().upper()


    registration = None

    error = None


    if rid:

        con = db()


        registration = con.execute(

            """

            SELECT *

            FROM registrations

            WHERE registration_id = ?

            """,

            (rid,)

        ).fetchone()


        con.close()


        if registration is None:

            error = "Registration ID not found."


    body = """

<div class="card">

<h2>
    🔎 Check Registration
</h2>


<form method="get">


<label>
    Registration ID
</label>


<input
    name="rid"
    value="{{ rid }}"
    placeholder="Example: NA-A1B2C3D4"
    required
>


<button type="submit">

    CHECK STATUS

</button>


</form>


{% if error %}

<div class="error">

    ❌ {{ error }}

</div>

{% endif %}


{% if registration %}

<div class="card">

<h2>
    📋 Registration Details
</h2>


<div class="data">

<b>
    Registration ID:
</b>

{{ registration["registration_id"] }}

<br>


<b>
    Player Name:
</b>

{{ registration["player_name"] }}

<br>


<b>
    Game UID:
</b>

{{ registration["player_uid"] }}

<br>


<b>
    Tournament:
</b>

{{ registration["tournament"] }}

<br>


<b>
    Entry Fee:
</b>

₹{{ registration["entry_fee"] }}

<br>


<b>
    Transaction ID:
</b>

{{ registration["transaction_id"] }}

<br>


<b>
    Submitted:
</b>

{{ registration["created_at"] }}

</div>


{% if registration["status"] == "APPROVED" %}

<div class="status approved">

    🟢 APPROVED

</div>


<div class="notice">

🎮 Your registration has been
approved by the administrator.

</div>


{% elif registration["status"] == "REJECTED" %}

<div class="status rejected">

    🔴 REJECTED

</div>


<div class="notice">

Your registration was rejected
by the administrator.

</div>


{% else %}

<div class="status pending">

    🟡 PENDING VERIFICATION

</div>


<div class="notice">

Your registration is saved and waiting
for administrator verification.

</div>


{% endif %}

</div>

{% endif %}


<a class="secondary"
   href="/">

    ← Back to Home

</a>

</div>

"""


    return render_template_string(

        page(
            "Registration Status",
            body
        ),

        rid=rid,

        registration=registration,

        error=error

    )


# =========================================================
# ADMIN LOGIN
# =========================================================

@app.route(
    "/admin/login",
    methods=["GET", "POST"]
)
def admin_login():

    if session.get("admin"):

        return redirect(
            url_for("admin")
        )


    error = None


    if request.method == "POST":

        password = request.form.get(
            "password",
            ""
        )


        if password == ADMIN_PASSWORD:

            session["admin"] = True

            return redirect(
                url_for("admin")
            )


        error = "Incorrect password."


    body = """

<div class="card">

<h2>
    🔐 Admin Login
</h2>


{% if error %}

<div class="error">

    ❌ {{ error }}

</div>

{% endif %}


<form method="post">


<label>
    Admin Password
</label>


<input
    type="password"
    name="password"
    placeholder="Enter admin password"
    required
>


<button type="submit">

    🔐 LOGIN

</button>


</form>


<a class="secondary"
   href="/">

    ← Back to Home

</a>

</div>

"""


    return render_template_string(

        page(
            "Admin Login",
            body
        ),

        error=error

    )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/admin")
def admin():

    if not session.get("admin"):

        return redirect(
            url_for("admin_login")
        )


    con = db()


    registrations = con.execute(

        """

        SELECT *

        FROM registrations

        ORDER BY id DESC

        """

    ).fetchall()


    con.close()


    body = """

<div class="card">

<h2>
    📊 Admin Dashboard
</h2>


<p class="small">

Total registrations:
{{ registrations|length }}

</p>


{% if not registrations %}

<div class="notice">

No registrations yet.

</div>

{% endif %}


{% for r in registrations %}


<div class="admin-item

{% if r['status'] == 'PENDING' %}

pending-border

{% elif r['status'] == 'APPROVED' %}

approved-border

{% else %}

rejected-border

{% endif %}

">


<h3>

👤 {{ r["player_name"] }}

</h3>


<div class="data">


<b>
Registration:
</b>

{{ r["registration_id"] }}

<br>


<b>
Tournament:
</b>

{{ r["tournament"] }}

<br>


<b>
UID:
</b>

{{ r["player_uid"] }}

<br>


<b>
Phone:
</b>

{{ r["phone"] }}

<br>


<b>
Transaction ID:
</b>

{{ r["transaction_id"] }}

<br>


<b>
Entry Fee:
</b>

₹{{ r["entry_fee"] }}

<br>


<b>
Submitted:
</b>

{{ r["created_at"] }}

<br>


<b>
Status:
</b>

{{ r["status"] }}


</div>


{% if r["status"] == "PENDING" %}


<form
    method="post"
    action="/admin/update/{{ r['id'] }}"
>


<button
    class="approve"
    name="status"
    value="APPROVED"
>

✓ APPROVE

</button>


<button
    class="reject"
    name="status"
    value="REJECTED"
>

✕ REJECT

</button>


</form>


{% endif %}


</div>


{% endfor %}


</div>


<a class="secondary"
   href="/admin/logout">

    🚪 LOGOUT

</a>

"""


    return render_template_string(

        page(
            "Admin Dashboard",
            body
        ),

        registrations=registrations

    )


# =========================================================
# ADMIN UPDATE
# =========================================================

@app.route(
    "/admin/update/<int:registration_id>",
    methods=["POST"]
)
def update_registration(
    registration_id
):

    if not session.get("admin"):

        return redirect(
            url_for("admin_login")
        )


    status_value = request.form.get(
        "status",
        ""
    )


    if status_value not in (
        "APPROVED",
        "REJECTED"
    ):

        return "Invalid status.", 400


    con = db()


    con.execute(

        """

        UPDATE registrations

        SET status = ?

        WHERE id = ?

        """,

        (
            status_value,
            registration_id
        )

    )


    con.commit()

    con.close()


    return redirect(
        url_for("admin")
    )


# =========================================================
# ADMIN LOGOUT
# =========================================================

@app.route("/admin/logout")
def admin_logout():

    session.clear()

    return redirect(
        url_for("home")
    )


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    init_db()

    print()
    print("=" * 45)
    print("⚡ NEON ARENA")
    print("=" * 45)

    print()
    print("Player:")
    print("http://127.0.0.1:5000")

    print()
    print("Admin:")
    print("http://127.0.0.1:5000/admin")

    print()
    print("Admin Password:")
    print(ADMIN_PASSWORD)

    print()
    print("=" * 45)

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )