import os
import re
from flask import Flask, render_template, request, jsonify

# Always use the templates folder beside this app.py file.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR)

# College information supplied for this student project.
# Confirm current details before publishing the website.

CONTACT = (
    "Phone: 0217-2627227\n"
    "Email: office@sswcoe.edu.in\n"
    "Website: https://sswcoe.edu.in/index.html"
)

FAQS = [
    (
        ["fee", "fees", "payment", "charges"],
        "Current course fees and hostel charges are not confirmed "
        "in this project.\n\n"
        "Please contact the college office for the latest details.\n\n"
        + CONTACT
    ),
    (
        ["admission", "admissions", "apply", "application",
         "eligibility", "cutoff", "seats", "deadline"],
        "SSWCOE's institute code is 06938.\n\n"
        "For current admission procedures, eligibility, cutoffs "
        "and available seats, check official notices or contact "
        "the college office.\n\n" + CONTACT
    ),
    (
        ["hostel", "accommodation", "mess"],
        "The supplied information describes a women's hostel "
        "with mess, Wi-Fi, computer facilities and security.\n\n"
        "Confirm current room availability, charges and rules "
        "with the college office.\n\n" + CONTACT
    ),
    (
        ["placement", "placements", "internship", "internships",
         "recruiters", "package", "siddhcamp"],
        "The supplied college information mentions Training "
        "& Placement support and a portal called SiddhCamp.\n\n"
        "For current recruiters, internships and placement "
        "statistics, contact the placement cell through "
        "the college office.\n\n" + CONTACT
    ),
    (
        ["library", "books"],
        "Current library timings and borrowing rules are "
        "not included in the supplied information.\n\n"
        "Please confirm them with the college library or office.\n\n"
        + CONTACT
    ),
    (
        ["transport", "bus", "buses"],
        "Current transport availability, routes and charges "
        "are not confirmed in this project.\n\n"
        "Please contact the college office.\n\n" + CONTACT
    ),
    (
        ["scholarship", "scholarships"],
        "Please contact the college office for current "
        "scholarship schemes, eligibility and deadlines.\n\n"
        + CONTACT
    ),
    (
        ["address", "location", "located", "reach"],
        "College address:\n\n"
        "T.P.S. II, Final Plot No. 74,\n"
        "Bhavani Peth, Rupa Bhavani Mandir Road,\n"
        "Solapur, Maharashtra - 413002."
    ),
    (
        ["affiliation", "affiliated", "university", "dbatu"],
        "SSWCOE is affiliated with Dr. Babasaheb Ambedkar "
        "Technological University (DBATU), Lonere."
    ),
    (
        ["code", "06938", "6938"],
        "SSWCOE's institute code is 06938, also written as 6938."
    ),
    (
        ["course", "courses", "branch", "branches", "department",
         "departments", "program", "programs", "cse", "ai", "ds",
         "electrical", "electronics"],
        "The supplied information lists these programs:\n\n"
        "• Computer Science & Engineering\n"
        "• CSE - Artificial Intelligence & Data Science\n"
        "• Electrical Engineering\n"
        "• Electronics & Telecommunication Engineering\n"
        "• Electronics & Computer Engineering\n\n"
        "Confirm current availability and intake with the college."
    ),
    (
        ["management", "trust", "devasthan"],
        "SSWCOE is managed by Shri Siddheshwar Devasthan, Solapur."
    ),
    (
        ["established", "founded", "establishment"],
        "According to the supplied information, SSWCOE was "
        "established in the academic year 2019-20."
    ),
    (
        ["autonomous", "autonomy"],
        "The supplied information describes SSWCOE as "
        "non-autonomous and affiliated with DBATU.\n\n"
        "Confirm any recent changes with the college."
    ),
    (
        ["naac", "nba", "accreditation"],
        "NAAC/NBA accreditation details are not verified in this "
        "project. Please check the latest official college documents."
    ),
    (
        ["timing", "timings", "hours"],
        "Current college and office timings are not confirmed "
        "in this project.\n\n"
        "Please contact the college office.\n\n" + CONTACT
    ),
    (
        ["contact", "phone", "email", "website", "telephone"],
        "College contact details:\n\n" + CONTACT
    ),
    (
        ["about", "sswcoe", "women", "girls"],
        "SSWCOE stands for Shree Siddheshwar Women's College of "
        "Engineering, Solapur.\n\n"
        "It is a women's engineering college managed by "
        "Shri Siddheshwar Devasthan, Solapur.\n\n"
        "Established: 2019-20\n"
        "Affiliation: DBATU, Lonere\n"
        "Institute code: 06938"
    ),
]


def get_answer(message):
    words = set(re.findall(r"[a-z0-9]+", message.lower()))

    for keywords, answer in FAQS:
        if any(keyword in words for keyword in keywords):
            return answer

        if words & {"hi", "hii", "hiii", "hello", "helo", "hey", "hlo"}:
         return (
            "Hello! Welcome to the SSWCOE assistant.\n\n"
            "Ask me about courses, admissions, hostel, "
            "placements, affiliation or contact details."
        )

    if words & {"thanks", "thank"}:
        return "You're welcome! You can ask another college question."

    return (
        "I don't have confirmed information about that topic.\n\n"
        "Please ask one topic at a time, such as courses, "
        "admission, hostel or contact details.\n\n" + CONTACT
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"reply": "Please send a valid message."}), 400

    message = data.get("message", "")

    if not isinstance(message, str) or not message.strip():
        return jsonify({"reply": "Please type a question."}), 400

    if len(message) > 500:
        return jsonify({"reply": "Please keep your question under 500 characters."}), 400

    return jsonify({"reply": get_answer(message)})


# Stop the browser from showing an old saved copy of the page.
@app.after_request
def no_cache(response):
    response.headers["Cache-Control"] = "no-store"
    return response


if __name__ == "__main__":
    index_file = os.path.join(TEMPLATE_DIR, "index.html")

    print("Project folder:", BASE_DIR)
    print("Website file  :", index_file)

    if not os.path.exists(index_file):
        print("ERROR: templates/index.html was not found.")
        print("Create the templates folder and index.html file first.")
    else:
        print("Website file found!")
        print("Open this in your browser: http://127.0.0.1:5050")
        app.run(host="127.0.0.1", port=5050, debug=False)