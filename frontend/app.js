const API = window.location.port === "5500"
  ? "http://localhost:8000"
  : `http://${window.location.hostname}:30081`;

let currentUser = null;
let token = null;


// ====================
// LOGIN
// ====================

async function login() {

    const username =
        document.getElementById("username").value;

    const password =
        document.getElementById("password").value;

    try {

        const response = await fetch(
            `${API}/auth/login`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    username,
                    password
                })
            }
        );

        if (!response.ok) {
            throw new Error("Login failed");
        }

        const data = await response.json();

        token = data.access_token;

        currentUser = {
            id: data.user_id,
            name: data.name,
            role: data.role
        };

        document
            .getElementById("loginPage")
            .classList.add("hidden");

        document
            .getElementById("dashboard")
            .classList.remove("hidden");

        document.getElementById("userName").textContent =
            currentUser.name;

        document.getElementById("userRole").textContent =
            currentUser.role;


        // Show manager controls

        if (
            currentUser.role === "MANAGER" ||
            currentUser.role === "ADMIN"
        ) {

            document
                .getElementById("managerButton")
                .classList.remove("hidden");
        }

    } catch (error) {

        document.getElementById("loginMessage").textContent =
            "Invalid username or password";
    }
}


// ====================
// LOGOUT
// ====================

function logout() {

    token = null;

    currentUser = null;

    document
        .getElementById("dashboard")
        .classList.add("hidden");

    document
        .getElementById("loginPage")
        .classList.remove("hidden");
}


// ====================
// LEAVE FORM
// ====================

function showLeaveForm() {

    document
        .getElementById("leaveForm")
        .classList.remove("hidden");
}


// ====================
// APPLY LEAVE
// ====================

async function applyLeave() {

    const leave = {

        employee_id: currentUser.id,

        employee_name: currentUser.name,

        leave_type:
            document.getElementById("leaveType").value,

        from_date:
            document.getElementById("fromDate").value,

        to_date:
            document.getElementById("toDate").value,

        reason:
            document.getElementById("reason").value
    };


    const response = await fetch(
        `${API}/leaves`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },

            body: JSON.stringify(leave)
        }
    );


    const data = await response.json();

    document.getElementById("content").innerHTML =
        `<h2>${data.message}</h2>`;

    loadLeaves();
}


// ====================
// MY LEAVE STATUS
// ====================

async function loadLeaves() {

    const response = await fetch(
        `${API}/leaves/${currentUser.id}`,
        {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );

    const leaves = await response.json();

    let html = "<h2>My Leave Requests</h2>";


    if (leaves.length === 0) {

        html += "<p>No leave requests found.</p>";

    } else {

        leaves.forEach(leave => {

            html += `
                <div class="item">

                    <b>${leave.leave_type}</b>

                    <p>
                        ${leave.from_date}
                        →
                        ${leave.to_date}
                    </p>

                    <p>
                        Reason:
                        ${leave.reason}
                    </p>

                    <span class="status ${leave.status.toLowerCase()}">
                        ${leave.status}
                    </span>

                </div>
            `;
        });
    }


    document.getElementById("content").innerHTML =
        html;
}


// ====================
// MANAGER - ALL LEAVES
// ====================

async function loadAllLeaves() {

    const response = await fetch(
        `${API}/leaves`,
        {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );

    const leaves = await response.json();

    let html = "<h2>Leave Requests</h2>";


    leaves.forEach(leave => {

        html += `
            <div class="item">

                <b>${leave.employee_name}</b>

                <p>
                    ${leave.leave_type}
                </p>

                <p>
                    ${leave.from_date}
                    →
                    ${leave.to_date}
                </p>

                <p>
                    Status:
                    <b>${leave.status}</b>
                </p>

                ${
                    leave.status === "PENDING"
                    ?
                    `
                    <button
                        onclick="updateLeave(${leave.id}, 'approve')"
                    >
                        Approve
                    </button>

                    <button
                        onclick="updateLeave(${leave.id}, 'reject')"
                    >
                        Reject
                    </button>
                    `
                    :
                    ""
                }

            </div>
        `;
    });


    document.getElementById("content").innerHTML =
        html;
}


// ====================
// APPROVE / REJECT
// ====================

async function updateLeave(id, action) {

    await fetch(
        `${API}/leaves/${id}/${action}`,
        {
            method: "PUT",

            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );

    loadAllLeaves();
}


// ====================
// PAYROLL
// ====================

async function loadPayroll() {

    const response = await fetch(
        `${API}/payroll/${currentUser.id}`,
        {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );

    const records = await response.json();

    let html = "<h2>Payroll Information</h2>";


    if (records.length === 0) {

        html += "<p>No payroll records found.</p>";

    } else {

        records.forEach(record => {

            html += `
                <div class="item">

                    <p>
                        <b>Month:</b>
                        ${record.month}
                    </p>

                    <p>
                        Basic Salary:
                        ₹${record.basic_salary}
                    </p>

                    <p>
                        Allowances:
                        ₹${record.allowances}
                    </p>

                    <p>
                        Deductions:
                        ₹${record.deductions}
                    </p>

                    <h3>
                        Net Salary:
                        ₹${record.net_salary}
                    </h3>

                    <span class="status approved">
                        ${record.status}
                    </span>

                </div>
            `;
        });
    }


    document.getElementById("content").innerHTML =
        html;
}
