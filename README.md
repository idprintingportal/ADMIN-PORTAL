<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ID Card Printing Portal — Admin</title>

<style>
:root{
    --bg:#070a10;
    --sidebar:#0d1119;
    --card:#111722;
    --card2:#151c28;
    --border:#232c3b;
    --text:#f5f7fb;
    --muted:#8993a5;
    --primary:#6d63ff;
    --primary2:#8d85ff;
    --green:#29c88a;
    --red:#ff5e73;
    --yellow:#f5b942;
    --shadow:0 20px 50px rgba(0,0,0,.25);
}

*{
    box-sizing:border-box;
    margin:0;
    padding:0;
    font-family:Inter,Arial,sans-serif;
}

body{
    background:var(--bg);
    color:var(--text);
    min-height:100vh;
}

/* ================= LOGIN ================= */

#loginPage{
    min-height:100vh;
    display:flex;
    align-items:center;
    justify-content:center;
    padding:20px;
    background:
        radial-gradient(circle at 20% 20%,rgba(109,99,255,.14),transparent 30%),
        radial-gradient(circle at 80% 80%,rgba(109,99,255,.10),transparent 30%),
        var(--bg);
}

.login-box{
    width:420px;
    max-width:100%;
    background:rgba(17,23,34,.92);
    border:1px solid var(--border);
    border-radius:22px;
    padding:35px;
    box-shadow:var(--shadow);
}

.brand{
    text-align:center;
    margin-bottom:30px;
}

.brand-icon{
    width:58px;
    height:58px;
    margin:0 auto 15px;
    display:flex;
    align-items:center;
    justify-content:center;
    border-radius:16px;
    background:linear-gradient(135deg,var(--primary),#948cff);
    font-size:20px;
    font-weight:800;
}

.brand h1{
    font-size:22px;
}

.brand p{
    color:var(--muted);
    font-size:12px;
    margin-top:7px;
}

.form-group{
    margin-bottom:17px;
}

.form-group label{
    display:block;
    color:#b7bfcc;
    font-size:12px;
    margin-bottom:8px;
}

input,select{
    width:100%;
    background:#0c1119;
    border:1px solid #293345;
    color:white;
    padding:13px 14px;
    border-radius:10px;
    outline:none;
}

input:focus,select:focus{
    border-color:var(--primary);
}

.login-btn{
    width:100%;
    padding:13px;
    border:0;
    border-radius:10px;
    background:linear-gradient(135deg,var(--primary),var(--primary2));
    color:white;
    font-weight:700;
    cursor:pointer;
    margin-top:5px;
}

.login-btn:hover{
    opacity:.9;
}

.login-error{
    color:var(--red);
    font-size:12px;
    text-align:center;
    margin-top:14px;
    min-height:16px;
}

.demo-info{
    margin-top:22px;
    padding:12px;
    border:1px solid var(--border);
    background:#0d121b;
    border-radius:10px;
    color:var(--muted);
    font-size:11px;
    line-height:1.6;
}

/* ================= APP ================= */

#adminApp{
    display:none;
    min-height:100vh;
}

.sidebar{
    width:255px;
    position:fixed;
    top:0;
    bottom:0;
    left:0;
    background:var(--sidebar);
    border-right:1px solid var(--border);
    padding:22px 15px;
}

.logo{
    display:flex;
    align-items:center;
    gap:11px;
    padding:7px 10px 27px;
}

.logo-icon{
    width:40px;
    height:40px;
    border-radius:11px;
    background:linear-gradient(135deg,var(--primary),#938cff);
    display:flex;
    align-items:center;
    justify-content:center;
    font-weight:800;
}

.logo-title{
    font-size:14px;
    font-weight:700;
}

.logo-title span{
    display:block;
    color:var(--muted);
    font-size:9px;
    font-weight:400;
    margin-top:4px;
}

.menu-label{
    color:#596476;
    font-size:10px;
    text-transform:uppercase;
    letter-spacing:1.3px;
    padding:10px 12px;
}

.nav{
    padding:4px 0;
}

.nav-item{
    padding:12px 13px;
    margin:3px 0;
    border-radius:9px;
    color:#a8b1c0;
    font-size:13px;
    cursor:pointer;
    display:flex;
    align-items:center;
    gap:12px;
}

.nav-item:hover{
    background:#151b26;
    color:white;
}

.nav-item.active{
    background:#1b1a37;
    border:1px solid #302c62;
    color:white;
}

.nav-icon{
    width:20px;
    text-align:center;
}

.logout{
    position:absolute;
    bottom:20px;
    left:15px;
    right:15px;
    color:#ff7788;
}

/* MAIN */

.main{
    margin-left:255px;
    padding:27px;
}

.topbar{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:27px;
}

.top-title h1{
    font-size:24px;
}

.top-title p{
    color:var(--muted);
    font-size:12px;
    margin-top:5px;
}

.admin-profile{
    display:flex;
    align-items:center;
    gap:10px;
    padding:8px 12px;
    background:var(--card);
    border:1px solid var(--border);
    border-radius:10px;
}

.avatar{
    width:32px;
    height:32px;
    border-radius:9px;
    background:#27224e;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:12px;
    font-weight:700;
}

.profile-name{
    font-size:12px;
}

.profile-role{
    display:block;
    color:var(--muted);
    font-size:9px;
    margin-top:2px;
}

/* STATS */

.stats{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:15px;
    margin-bottom:20px;
}

.stat-card{
    background:var(--card);
    border:1px solid var(--border);
    border-radius:15px;
    padding:19px;
}

.stat-top{
    display:flex;
    justify-content:space-between;
    align-items:center;
}

.stat-label{
    color:var(--muted);
    font-size:11px;
}

.stat-icon{
    width:31px;
    height:31px;
    display:flex;
    align-items:center;
    justify-content:center;
    border-radius:8px;
    background:#1c1b39;
}

.stat-number{
    font-size:24px;
    font-weight:700;
    margin-top:12px;
}

.stat-note{
    color:var(--muted);
    font-size:10px;
    margin-top:5px;
}

/* CONTENT */

.panel{
    background:var(--card);
    border:1px solid var(--border);
    border-radius:16px;
    overflow:hidden;
}

.panel-header{
    padding:19px;
    display:flex;
    justify-content:space-between;
    align-items:center;
    border-bottom:1px solid var(--border);
}

.panel-header h2{
    font-size:15px;
}

.panel-header p{
    color:var(--muted);
    font-size:10px;
    margin-top:5px;
}

.filters{
    display:flex;
    gap:10px;
}

.filters input{
    width:210px;
    padding:9px 11px;
    font-size:11px;
}

.filters select{
    width:130px;
    padding:9px 11px;
    font-size:11px;
}

.table-wrap{
    overflow-x:auto;
}

table{
    width:100%;
    border-collapse:collapse;
    min-width:800px;
}

th{
    text-align:left;
    color:#697487;
    font-size:10px;
    text-transform:uppercase;
    letter-spacing:.5px;
    padding:13px 18px;
    border-bottom:1px solid var(--border);
}

td{
    padding:15px 18px;
    font-size:12px;
    border-bottom:1px solid #1b2330;
}

tr:hover td{
    background:#131a25;
}

.distributor{
    display:flex;
    align-items:center;
    gap:10px;
}

.distributor-avatar{
    width:34px;
    height:34px;
    border-radius:9px;
    background:#20263a;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:11px;
    font-weight:700;
}

.distributor-name{
    font-weight:600;
}

.distributor-email{
    color:var(--muted);
    font-size:10px;
    margin-top:3px;
}

.badge{
    display:inline-flex;
    align-items:center;
    padding:5px 9px;
    border-radius:6px;
    font-size:9px;
    font-weight:600;
}

.badge-active{
    background:#11281f;
    color:#5edba7;
}

.badge-inactive{
    background:#29151a;
    color:#ff7385;
}

.badge-paid{
    background:#11281f;
    color:#5edba7;
}

.badge-pending{
    background:#2a2111;
    color:#f1bd54;
}

.amount{
    font-weight:600;
}

.pending{
    color:var(--yellow);
}

.paid{
    color:var(--green);
}

.action-btn{
    padding:6px 9px;
    border-radius:6px;
    border:1px solid var(--border);
    background:#171e2a;
    color:white;
    cursor:pointer;
    font-size:10px;
}

.action-btn:hover{
    border-color:var(--primary);
}

/* EMPTY */

.empty{
    padding:45px;
    text-align:center;
    color:var(--muted);
    font-size:12px;
}

/* MOBILE */

.mobile-header{
    display:none;
}

@media(max-width:1000px){

    .stats{
        grid-template-columns:repeat(2,1fr);
    }

}

@media(max-width:700px){

    .sidebar{
        display:none;
    }

    .main{
        margin-left:0;
        padding:18px;
    }

    .mobile-header{
        display:block;
        margin-bottom:15px;
    }

    .stats{
        grid-template-columns:1fr 1fr;
    }

    .topbar{
        align-items:flex-start;
    }

    .filters{
        margin-top:10px;
        width:100%;
        flex-direction:column;
    }

    .filters input,
    .filters select{
        width:100%;
    }

    .panel-header{
        display:block;
    }

}
</style>
</head>

<body>


<!-- ================= LOGIN ================= -->

<section id="loginPage">

    <div class="login-box">

        <div class="brand">

            <div class="brand-icon">
                ID
            </div>

            <h1>Admin Portal</h1>

            <p>
                ID Card Printing Portal
            </p>

        </div>


        <form onsubmit="login(event)">

            <div class="form-group">

                <label>Admin Email</label>

                <input
                    id="email"
                    type="email"
                    placeholder="admin@example.com"
                    required
                >

            </div>


            <div class="form-group">

                <label>Password</label>

                <input
                    id="password"
                    type="password"
                    placeholder="Enter password"
                    required
                >

            </div>


            <button class="login-btn" type="submit">
                Login to Admin Portal
            </button>

            <div id="loginError" class="login-error"></div>

        </form>


        <div class="demo-info">

            <strong>Demo Credentials</strong><br>

            Email: admin@idcardportal.com<br>
            Password: Admin@123

        </div>

    </div>

</section>



<!-- ================= ADMIN APP ================= -->

<section id="adminApp">


    <!-- SIDEBAR -->

    <aside class="sidebar">

        <div class="logo">

            <div class="logo-icon">
                ID
            </div>

            <div class="logo-title">

                ID Card Printing

                <span>
                    ADMIN CONTROL CENTER
                </span>

            </div>

        </div>


        <div class="menu-label">
            Management
        </div>


        <div
            class="nav-item active"
            onclick="showSection('dashboard',this)"
        >
            <span class="nav-icon">⌂</span>
            Dashboard
        </div>


        <div
            class="nav-item"
            onclick="showSection('distributors',this)"
        >
            <span class="nav-icon">◉</span>
            Distributors
        </div>


        <div
            class="nav-item"
            onclick="showSection('payments',this)"
        >
            <span class="nav-icon">₹</span>
            Payments
        </div>


        <div class="menu-label">
            System
        </div>


        <div
            class="nav-item"
            onclick="showSection('settings',this)"
        >
            <span class="nav-icon">⚙</span>
            Settings
        </div>


        <div
            class="nav-item logout"
            onclick="logout()"
        >
            <span class="nav-icon">↪</span>
            Logout
        </div>

    </aside>



    <!-- MAIN -->

    <main class="main">

        <div class="mobile-header">
            <strong>ID Card Printing Portal</strong>
        </div>


        <div class="topbar">

            <div class="top-title">

                <h1 id="sectionTitle">
                    Admin Dashboard
                </h1>

                <p id="sectionDescription">
                    Manage distributors, payments and portal activity.
                </p>

            </div>


            <div class="admin-profile">

                <div class="avatar">
                    AD
                </div>

                <div class="profile-name">

                    Administrator

                    <span class="profile-role">
                        Super Admin
                    </span>

                </div>

            </div>

        </div>


        <!-- ================= CONTENT ================= -->

        <div id="pageContent"></div>

    </main>

</section>



<script>

/* =========================================
   DEMO DATA
========================================= */

const distributors = [

    {
        id:1,
        name:"Shree Digital Services",
        email:"shree@example.com",
        phone:"+91 98765 43210",
        status:"Active",
        payment:"Paid",
        amount:12500,
        pending:0
    },

    {
        id:2,
        name:"Maharashtra Online Center",
        email:"moc@example.com",
        phone:"+91 98220 11223",
        status:"Active",
        payment:"Pending",
        amount:8000,
        pending:8000
    },

    {
        id:3,
        name:"Sai Document Point",
        email:"sai@example.com",
        phone:"+91 97654 22331",
        status:"Active",
        payment:"Paid",
        amount:15000,
        pending:0
    },

    {
        id:4,
        name:"City Xerox & Print",
        email:"cityprint@example.com",
        phone:"+91 99887 66554",
        status:"Inactive",
        payment:"Pending",
        amount:6500,
        pending:6500
    },

    {
        id:5,
        name:"Smart CSC Center",
        email:"smartcsc@example.com",
        phone:"+91 90909 11223",
        status:"Active",
        payment:"Paid",
        amount:11200,
        pending:0
    }

];


/* =========================================
   LOGIN
========================================= */

function login(event){

    event.preventDefault();

    const email =
        document.getElementById("email").value.trim();

    const password =
        document.getElementById("password").value;

    const error =
        document.getElementById("loginError");


    /*
       DEMO ONLY

       Production version:
       authenticate against backend API.
    */

    if(
        email === "admin@idcardportal.com" &&
        password === "Admin@123"
    ){

        sessionStorage.setItem(
            "adminLoggedIn",
            "true"
        );

        document.getElementById("loginPage")
            .style.display="none";

        document.getElementById("adminApp")
            .style.display="block";

        renderDashboard();

    }else{

        error.innerText =
            "Invalid admin email or password.";

    }

}


/* =========================================
   LOGOUT
========================================= */

function logout(){

    sessionStorage.removeItem("adminLoggedIn");

    document.getElementById("adminApp")
        .style.display="none";

    document.getElementById("loginPage")
        .style.display="flex";

    document.getElementById("email").value="";
    document.getElementById("password").value="";

}


/* =========================================
   CHECK SESSION
========================================= */

window.onload=function(){

    if(
        sessionStorage.getItem("adminLoggedIn")
        === "true"
    ){

        document.getElementById("loginPage")
            .style.display="none";

        document.getElementById("adminApp")
            .style.display="block";

        renderDashboard();

    }else{

        document.getElementById("loginPage")
            .style.display="flex";

        document.getElementById("adminApp")
            .style.display="none";

    }

};


/* =========================================
   SECTION SWITCH
========================================= */

function showSection(section,element){

    document.querySelectorAll(".nav-item")
        .forEach(item =>
            item.classList.remove("active")
        );

    if(element){
        element.classList.add("active");
    }


    if(section==="dashboard"){

        renderDashboard();

    }

    else if(section==="distributors"){

        renderDistributors();

    }

    else if(section==="payments"){

        renderPayments();

    }

    else if(section==="settings"){

        renderSettings();

    }

}


/* =========================================
   DASHBOARD
========================================= */

function renderDashboard(){

    document.getElementById("sectionTitle")
        .innerText="Admin Dashboard";

    document.getElementById("sectionDescription")
        .innerText=
        "Manage distributors, payments and portal activity.";


    const active =
        distributors.filter(
            d=>d.status==="Active"
        ).length;


    const pending =
        distributors.reduce(
            (sum,d)=>sum+d.pending,
            0
        );


    const total =
        distributors.reduce(
            (sum,d)=>sum+d.amount,
            0
        );


    document.getElementById("pageContent").innerHTML=`

        <div class="stats">

            <div class="stat-card">

                <div class="stat-top">

                    <span class="stat-label">
                        Total Distributors
                    </span>

                    <span class="stat-icon">
                        ◉
                    </span>

                </div>

                <div class="stat-number">
                    ${distributors.length}
                </div>

                <div class="stat-note">
                    Registered distributors
                </div>

            </div>


            <div class="stat-card">

                <div class="stat-top">

                    <span class="stat-label">
                        Active
                    </span>

                    <span class="stat-icon">
                        ✓
                    </span>

                </div>

                <div class="stat-number">
                    ${active}
                </div>

                <div class="stat-note">
                    Currently active
                </div>

            </div>


            <div class="stat-card">

                <div class="stat-top">

                    <span class="stat-label">
                        Total Revenue
                    </span>

                    <span class="stat-icon">
                        ₹
                    </span>

                </div>

                <div class="stat-number">
                    ₹${total.toLocaleString("en-IN")}
                </div>

                <div class="stat-note">
                    Distributor payments
                </div>

            </div>


            <div class="stat-card">

                <div class="stat-top">

                    <span class="stat-label">
                        Pending
                    </span>

                    <span class="stat-icon">
                        !
                    </span>

                </div>

                <div class="stat-number pending">
                    ₹${pending.toLocaleString("en-IN")}
                </div>

                <div class="stat-note">
                    Outstanding payments
                </div>

            </div>

        </div>


        <div class="panel">

            <div class="panel-header">

                <div>

                    <h2>
                        Recent Distributors
                    </h2>

                    <p>
                        Latest distributor activity
                    </p>

                </div>

            </div>


            <div class="table-wrap">

                ${createDistributorTable(
                    distributors.slice(0,5)
                )}

            </div>

        </div>

    `;

}


/* =========================================
   DISTRIBUTORS
========================================= */

function renderDistributors(){

    document.getElementById("sectionTitle")
        .innerText="Distributors";

    document.getElementById("sectionDescription")
        .innerText=
        "View and manage all connected distributors.";


    document.getElementById("pageContent").innerHTML=`

        <div class="panel">

            <div class="panel-header">

                <div>

                    <h2>
                        Distributor Management
                    </h2>

                    <p>
                        ${distributors.length}
                        distributors registered
                    </p>

                </div>


                <div class="filters">

                    <input
                        id="searchDistributor"
                        placeholder="Search distributor..."
                        oninput="filterDistributors()"
                    >


                    <select
                        id="statusFilter"
                        onchange="filterDistributors()"
                    >

                        <option value="All">
                            All Status
                        </option>

                        <option value="Active">
                            Active
                        </option>

                        <option value="Inactive">
                            Inactive
                        </option>

                    </select>

                </div>

            </div>


            <div
                class="table-wrap"
                id="distributorTable"
            >

                ${createDistributorTable(distributors)}

            </div>

        </div>

    `;

}


/* =========================================
   TABLE
========================================= */

function createDistributorTable(list){

    if(!list.length){

        return `
            <div class="empty">
                No distributors found.
            </div>
        `;

    }


    return `

        <table>

            <thead>

                <tr>

                    <th>
                        Distributor
                    </th>

                    <th>
                        Contact
                    </th>

                    <th>
                        Status
                    </th>

                    <th>
                        Payment
                    </th>

                    <th>
                        Amount
                    </th>

                    <th>
                        Action
                    </th>

                </tr>

            </thead>


            <tbody>

                ${list.map(d=>`

                    <tr>

                        <td>

                            <div class="distributor">

                                <div class="distributor-avatar">
                                    ${getInitials(d.name)}
                                </div>

                                <div>

                                    <div class="distributor-name">
                                        ${d.name}
                                    </div>

                                    <div class="distributor-email">
                                        ${d.email}
                                    </div>

                                </div>

                            </div>

                        </td>


                        <td>
                            ${d.phone}
                        </td>


                        <td>

                            <span class="badge
                                ${d.status==="Active"
                                ?"badge-active"
                                :"badge-inactive"}">

                                ${d.status}

                            </span>

                        </td>


                        <td>

                            <span class="badge
                                ${d.payment==="Paid"
                                ?"badge-paid"
                                :"badge-pending"}">

                                ${d.payment}

                            </span>

                        </td>


                        <td>

                            <span class="amount">
                                ₹${d.amount.toLocaleString("en-IN")}
                            </span>

                            ${
                                d.pending > 0
                                ?
                                `<div class="pending">
                                    Pending ₹${d.pending.toLocaleString("en-IN")}
                                </div>`
                                :
                                `<div class="paid">
                                    Fully Paid
                                </div>`
                            }

                        </td>


                        <td>

                            <button
                                class="action-btn"
                                onclick="viewDistributor(${d.id})"
                            >
                                View
                            </button>

                        </td>

                    </tr>

                `).join("")}

            </tbody>

        </table>

    `;

}


/* =========================================
   SEARCH
========================================= */

function filterDistributors(){

    const search =
        document.getElementById(
            "searchDistributor"
        ).value.toLowerCase();


    const status =
        document.getElementById(
            "statusFilter"
        ).value;


    const filtered =
        distributors.filter(d=>{

            const matchesSearch =
                d.name.toLowerCase()
                    .includes(search) ||
                d.email.toLowerCase()
                    .includes(search) ||
                d.phone.includes(search);


            const matchesStatus =
                status==="All" ||
                d.status===status;


            return matchesSearch && matchesStatus;

        });


    document.getElementById(
        "distributorTable"
    ).innerHTML =
        createDistributorTable(filtered);

}


/* =========================================
   VIEW DISTRIBUTOR
========================================= */

function viewDistributor(id){

    const d =
        distributors.find(x=>x.id===id);

    if(!d) return;


    alert(

        "Distributor Details\n\n" +

        "Name: " + d.name + "\n" +

        "Email: " + d.email + "\n" +

        "Mobile: " + d.phone + "\n" +

        "Status: " + d.status + "\n" +

        "Payment: " + d.payment + "\n" +

        "Amount: ₹" +
        d.amount.toLocaleString("en-IN") + "\n" +

        "Pending: ₹" +
        d.pending.toLocaleString("en-IN")

    );

}


/* =========================================
   PAYMENTS
========================================= */

function renderPayments(){

    document.getElementById("sectionTitle")
        .innerText="Payments";

    document.getElementById("sectionDescription")
        .innerText=
        "Track distributor payments and outstanding amounts.";


    const total =
        distributors.reduce(
            (sum,d)=>sum+d.amount,
            0
        );


    const pending =
        distributors.reduce(
            (sum,d)=>sum+d.pending,
            0
        );


    const received=total-pending;


    document.getElementById("pageContent").innerHTML=`

        <div class="stats">

            <div class="stat-card">

                <div class="stat-label">
                    Total Billing
                </div>

                <div class="stat-number">
                    ₹${total.toLocaleString("en-IN")}
                </div>

            </div>


            <div class="stat-card">

                <div class="stat-label">
                    Received
                </div>

                <div class="stat-number paid">
                    ₹${received.toLocaleString("en-IN")}
                </div>

            </div>


            <div class="stat-card">

                <div class="stat-label">
                    Pending
                </div>

                <div class="stat-number pending">
                    ₹${pending.toLocaleString("en-IN")}
                </div>

            </div>


            <div class="stat-card">

                <div class="stat-label">
                    Payment Records
                </div>

                <div class="stat-number">
                    ${distributors.length}
                </div>

            </div>

        </div>


        <div class="panel">

            <div class="panel-header">

                <div>

                    <h2>
                        Distributor Payments
                    </h2>

                    <p>
                        Payment status overview
                    </p>

                </div>

            </div>


            <div class="table-wrap">

                ${createPaymentTable()}

            </div>

        </div>

    `;

}


function createPaymentTable(){

    return `

        <table>

            <thead>

                <tr>

                    <th>
                        Distributor
                    </th>

                    <th>
                        Billing
                    </th>

                    <th>
                        Received
                    </th>

                    <th>
                        Pending
                    </th>

                    <th>
                        Status
                    </th>

                    <th>
                        Action
                    </th>

                </tr>

            </thead>


            <tbody>

                ${distributors.map(d=>{

                    const received =
                        d.amount-d.pending;

                    return `

                        <tr>

                            <td>
                                ${d.name}
                            </td>

                            <td>
                                ₹${d.amount.toLocaleString("en-IN")}
                            </td>

                            <td class="paid">
                                ₹${received.toLocaleString("en-IN")}
                            </td>

                            <td class="pending">
                                ₹${d.pending.toLocaleString("en-IN")}
                            </td>

                            <td>

                                <span class="badge
                                    ${d.payment==="Paid"
                                    ?"badge-paid"
                                    :"badge-pending"}">

                                    ${d.payment}

                                </span>

                            </td>

                            <td>

                                <button
                                    class="action-btn"
                                    onclick="recordPayment(${d.id})"
                                >
                                    Record Payment
                                </button>

                            </td>

                        </tr>

                    `;

                }).join("")}

            </tbody>

        </table>

    `;

}


/* =========================================
   RECORD PAYMENT
========================================= */

function recordPayment(id){

    const d =
        distributors.find(x=>x.id===id);

    if(!d) return;


    if(d.pending===0){

        alert(
            "This distributor has no pending payment."
        );

        return;

    }


    const amount =
        prompt(
            "Enter payment received:",
            d.pending
        );


    if(amount===null) return;


    const value =
        Number(amount);


    if(
        isNaN(value) ||
        value<=0 ||
        value>d.pending
    ){

        alert("Please enter a valid amount.");

        return;

    }


    d.pending-=value;


    if(d.pending===0){

        d.payment="Paid";

    }


    alert(
        "Payment recorded successfully."
    );


    renderPayments();

}


/* =========================================
   SETTINGS
========================================= */

function renderSettings(){

    document.getElementById("sectionTitle")
        .innerText="Settings";

    document.getElementById("sectionDescription")
        .innerText=
        "Admin portal configuration.";


    document.getElementById("pageContent").innerHTML=`

        <div class="panel">

            <div class="panel-header">

                <div>

                    <h2>
                        Portal Settings
                    </h2>

                    <p>
                        Basic configuration
                    </p>

                </div>

            </div>


            <div style="padding:20px">

                <div class="form-group">

                    <label>
                        Company Name
                    </label>

                    <input
                        value="ID Card Printing Portal"
                    >

                </div>


                <div class="form-group">

                    <label>
                        Support Email
                    </label>

                    <input
                        value="support@idcardportal.com"
                    >

                </div>


                <div class="form-group">

                    <label>
                        Support Mobile
                    </label>

                    <input
                        value="+91 90000 00000"
                    >

                </div>


                <button
                    class="login-btn"
                    style="width:auto;padding:11px 22px"
                    onclick="alert('Settings saved in prototype.')"
                >
                    Save Settings
                </button>

            </div>

        </div>

    `;

}


/* =========================================
   HELPERS
========================================= */

function getInitials(name){

    return name
        .split(" ")
        .slice(0,2)
        .map(word=>word[0])
        .join("")
        .toUpperCase();

}

</script>

</body>
</html>
