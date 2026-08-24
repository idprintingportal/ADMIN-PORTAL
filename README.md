<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>ID Card Printing Portal</title>

<style>
:root{
    --bg:#090812;
    --panel:#12111b;
    --panel2:#181624;
    --line:#302b3b;
    --text:#f7f4fb;
    --muted:#aaa3b3;
    --primary:#7a67ff;
    --secondary:#f05bd5;
    --green:#5edb9c;
    --red:#ff7182;
    --yellow:#ffc857;
}

*{
    box-sizing:border-box;
}

body{
    margin:0;
    background:
        radial-gradient(
            circle at 50% 0%,
            #28183d 0%,
            transparent 38%
        ),
        var(--bg);
    color:var(--text);
    font-family:Inter,Arial,system-ui,sans-serif;
}

button,
input,
select{
    font:inherit;
}

button{
    cursor:pointer;
}

.hidden{
    display:none!important;
}

/* =========================
   COMMON
========================= */

.container{
    width:100%;
    max-width:1450px;
    margin:auto;
    padding:20px;
}

.topbar{
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding:14px 0 20px;
    border-bottom:1px solid #4b3c51;
}

.logo{
    font-size:26px;
    font-weight:900;
    letter-spacing:.7px;
    background:linear-gradient(
        90deg,
        #ad8bff,
        #ff5bd5
    );
    -webkit-background-clip:text;
    color:transparent;
}

.top-actions{
    display:flex;
    gap:8px;
}

.btn{
    border:1px solid var(--line);
    background:#171522;
    color:white;
    padding:10px 15px;
    border-radius:11px;
    transition:.2s;
}

.btn:hover{
    border-color:#8a78ff;
    transform:translateY(-1px);
}

.btn-primary{
    background:
        linear-gradient(
            135deg,
            var(--primary),
            #9d72ff
        );
    border-color:#a18dff;
}

.btn-danger{
    background:#542c35;
    border-color:#88444f;
}

/* =========================
   LOGIN
========================= */

.login-page{
    min-height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    padding:20px;
}

.login-box{
    width:430px;
    max-width:100%;
    background:rgba(18,17,27,.95);
    border:1px solid var(--line);
    border-radius:22px;
    padding:32px;
    box-shadow:
        0 25px 80px rgba(0,0,0,.6);
}

.login-logo{
    text-align:center;
    font-size:28px;
    font-weight:900;
    background:
        linear-gradient(
            90deg,
            #aa87ff,
            #ff60d1
        );
    -webkit-background-clip:text;
    color:transparent;
}

.login-subtitle{
    text-align:center;
    color:var(--muted);
    margin-bottom:25px;
}

.field{
    margin:14px 0;
}

.field label{
    display:block;
    color:var(--muted);
    font-size:12px;
    margin-bottom:6px;
}

.field input,
.field select{
    width:100%;
    padding:11px;
    border-radius:9px;
    border:1px solid var(--line);
    background:#0d0c13;
    color:white;
    outline:none;
}

.field input:focus,
.field select:focus{
    border-color:#8170ff;
}

.login-btn{
    width:100%;
    margin-top:10px;
}

.login-bottom{
    display:flex;
    justify-content:center;
    gap:10px;
    margin-top:18px;
}

.login-error{
    text-align:center;
    min-height:20px;
    color:var(--red);
    margin-top:10px;
}

/* =========================
   TOOL BAR
========================= */

.tool-bar{
    display:flex;
    flex-wrap:wrap;
    justify-content:center;
    gap:9px;
    padding:20px 0;
}

.tool-btn{
    background:#171522;
    color:#fff;
    border:1px solid var(--line);
    padding:10px 14px;
    border-radius:11px;
}

.tool-btn:hover{
    border-color:#8271ff;
}

.tool-btn.active{
    background:
        linear-gradient(
            135deg,
            #5e86ff,
            #7c67ff
        );
    border-color:#9a9cff;
}

/* =========================
   ACCOUNT BAR
========================= */

.account-bar{
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:15px 20px;
    border:1px solid #46404f;
    border-radius:18px;
    background:#14121c;
}

.validity{
    border:1px solid #568b61;
    background:#15221a;
    color:#9ee9a2;
    border-radius:24px;
    padding:9px 15px;
}

.validity b{
    color:var(--yellow);
}

/* =========================
   HERO
========================= */

.hero{
    text-align:center;
    padding:30px 10px;
}

.hero h1{
    font-size:36px;
    margin:20px 0 10px;
    background:
        linear-gradient(
            90deg,
            #b887ff,
            #ff60d0
        );
    -webkit-background-clip:text;
    color:transparent;
}

.hero p{
    color:var(--muted);
}

.pill{
    display:inline-block;
    border:1px solid #6684a9;
    background:#182636;
    color:#a9dcff;
    padding:8px 18px;
    border-radius:24px;
    font-size:12px;
}

/* =========================
   CARDS
========================= */

.grid{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:18px;
}

.card{
    background:var(--panel);
    border:1px solid var(--line);
    border-radius:17px;
    padding:20px;
}

.drop-zone{
    min-height:180px;
    border:2px dashed #646b83;
    border-radius:15px;
    display:flex;
    justify-content:center;
    align-items:center;
    flex-direction:column;
    padding:20px;
    text-align:center;
}

.preview{
    display:block;
    max-width:100%;
    max-height:400px;
    margin:15px auto;
    border-radius:9px;
}

.controls{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:12px;
    margin-top:15px;
}

.actions{
    display:flex;
    justify-content:flex-end;
    gap:10px;
    margin-top:15px;
}

/* =========================
   ID CARD
========================= */

.print-sheet{
    background:white;
    padding:12px;
    display:grid;
    grid-template-columns:repeat(5,1fr);
    gap:2.5mm;
}

.id-card{
    aspect-ratio:1013 / 638;
    border:3px solid #000;
    overflow:hidden;
    background:#eee;
}

.id-card img{
    width:100%;
    height:100%;
    object-fit:cover;
}

/* =========================
   HISTORY
========================= */

.history-row{
    display:flex;
    justify-content:space-between;
    gap:20px;
    padding:13px 0;
    border-bottom:1px solid var(--line);
}

.note{
    color:var(--muted);
    font-size:12px;
}

/* =========================
   ADMIN
========================= */

.admin-layout{
    min-height:100vh;
    display:grid;
    grid-template-columns:230px 1fr;
}

.admin-sidebar{
    background:#0d0c14;
    border-right:1px solid var(--line);
    padding:18px;
}

.admin-sidebar h2{
    font-size:17px;
    margin-bottom:20px;
}

.admin-sidebar .btn{
    width:100%;
    margin:5px 0;
    text-align:left;
}

.admin-main{
    padding:25px;
}

.stats{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:12px;
}

.stat{
    background:var(--panel);
    border:1px solid var(--line);
    border-radius:15px;
    padding:18px;
}

.stat small{
    color:var(--muted);
}

.stat strong{
    display:block;
    font-size:25px;
    margin-top:8px;
}

/* =========================
   TABLE
========================= */

.table-wrapper{
    overflow:auto;
}

.table{
    width:100%;
    min-width:800px;
    border-collapse:collapse;
}

.table th,
.table td{
    text-align:left;
    padding:12px;
    border-bottom:1px solid var(--line);
}

.badge{
    padding:5px 8px;
    border-radius:7px;
    font-size:11px;
}

.badge-active{
    background:#153023;
    color:var(--green);
}

.badge-inactive{
    background:#3a1b22;
    color:var(--red);
}

/* =========================
   RESPONSIVE
========================= */

@media(max-width:900px){

    .grid{
        grid-template-columns:1fr;
    }

    .admin-layout{
        grid-template-columns:1fr;
    }

    .admin-sidebar{
        border-right:none;
        border-bottom:1px solid var(--line);
    }

    .stats{
        grid-template-columns:1fr 1fr;
    }
}

@media(max-width:600px){

    .logo{
        font-size:18px;
    }

    .topbar{
        gap:10px;
        align-items:flex-start;
        flex-direction:column;
    }

    .account-bar{
        flex-direction:column;
        align-items:flex-start;
        gap:10px;
    }

    .controls{
        grid-template-columns:1fr;
    }

    .stats{
        grid-template-columns:1fr;
    }

    .print-sheet{
        grid-template-columns:1fr;
    }
}
</style>
</head>

<body>

<div id="app"></div>

<script>

/* =========================================================
   API HELPER
========================================================= */

async function api(url, options = {}){

    const response = await fetch(url,{
        ...options,

        headers:
            options.body instanceof FormData
            ? options.headers
            : {
                "Content-Type":"application/json",
                ...(options.headers || {})
            }
    });

    const data =
        await response.json().catch(() => ({}));

    if(!response.ok){
        throw new Error(
            data.error || "Request failed"
        );
    }

    return data;
}


/* =========================================================
   ESCAPE HTML
========================================================= */

function escapeHTML(value){

    return String(value ?? "")
        .replace(/[&<>"']/g,function(char){

            return {
                "&":"&amp;",
                "<":"&lt;",
                ">":"&gt;",
                '"':"&quot;",
                "'":"&#039;"
            }[char];

        });
}


/* =========================================================
   START
========================================================= */

async function start(){

    try{

        const user =
            await api("/api/me");

        if(!user.loggedIn){

            showLogin();

            return;
        }

        if(user.role === "admin"){

            showAdmin();

        }else{

            showCustomer(user);
        }

    }catch(error){

        showLogin();
    }
}


/* =========================================================
   LOGIN
========================================================= */

let loginType = "customer";


function showLogin(){

    document.getElementById("app").innerHTML = `

    <div class="login-page">

        <div class="login-box">

            <div class="login-logo">
                ID CARD PRINTING PORTAL
            </div>

            <div class="login-subtitle">
                Secure Customer Portal
            </div>

            <div class="field">

                <label>
                    Username
                </label>

                <input
                    id="loginUsername"
                    type="text"
                    autocomplete="username"
                    placeholder="Enter username"
                >

            </div>

            <div class="field">

                <label>
                    Password
                </label>

                <input
                    id="loginPassword"
                    type="password"
                    autocomplete="current-password"
                    placeholder="Enter password"
                >

            </div>

            <button
                class="btn btn-primary login-btn"
                onclick="login()"
            >
                Login
            </button>

            <div
                id="loginError"
                class="login-error"
            ></div>

            <div class="login-bottom">

                <button
                    class="btn"
                    onclick="showHelp()"
                >
                    Help
                </button>

                <button
                    class="btn"
                    onclick="adminMode()"
                >
                    Admin Login
                </button>

            </div>

        </div>

    </div>

    `;
}


function adminMode(){

    loginType = "admin";

    document.querySelector(
        "#loginUsername"
    ).placeholder = "Admin Email";

    document.querySelector(
        "#loginUsername"
    ).previousElementSibling.innerText =
        "Admin Email";

    document.querySelector(
        ".login-subtitle"
    ).innerText =
        "Administrator Login";
}


async function login(){

    const username =
        document.getElementById(
            "loginUsername"
        ).value.trim();

    const password =
        document.getElementById(
            "loginPassword"
        ).value;

    const error =
        document.getElementById(
            "loginError"
        );

    error.innerText = "";

    if(!username || !password){

        error.innerText =
            "Username and password required.";

        return;
    }

    try{

        const result =
            await api("/api/login",{

                method:"POST",

                body:JSON.stringify({

                    type:loginType,

                    username,

                    password

                })

            });

        if(result.role === "admin"){

            showAdmin();

        }else{

            showCustomer(result);
        }

    }catch(err){

        error.innerText =
            err.message;
    }
}


/* =========================================================
   HELP
========================================================= */

async function showHelp(){

    try{

        const data =
            await api("/api/help");

        alert(
            "HELP\n\n" +
            "Email: " + data.email +
            "\nMobile: " + data.mobile
        );

    }catch(error){

        alert(
            "Please contact administrator."
        );
    }
}


/* =========================================================
   LOGOUT
========================================================= */

async function logout(){

    await api(
        "/api/logout",
        {
            method:"POST"
        }
    );

    start();
}


/* =========================================================
   CUSTOMER DASHBOARD
========================================================= */

function showCustomer(user){

    document.getElementById("app").innerHTML = `

    <div class="container">

        <div class="topbar">

            <div class="logo">
                ID CARD PRINT & CONVERTER PORTAL
            </div>

            <div class="top-actions">

                <button
                    class="btn"
                    onclick="showHelp()"
                >
                    Help
                </button>

                <button
                    class="btn btn-danger"
                    onclick="logout()"
                >
                    🔒 Logout
                </button>

            </div>

        </div>


        <div class="tool-bar">

            <button
                class="tool-btn"
                id="tool-id"
                onclick="openTool('id')"
            >
                🪪 ID Card (5 Slots)
            </button>

            <button
                class="tool-btn"
                id="tool-passport"
                onclick="openTool('passport')"
            >
                👤 Passport Photos
            </button>

            <button
                class="tool-btn"
                onclick="openTool('name')"
            >
                📄 Name & Date Passport
            </button>

            <button
                class="tool-btn"
                onclick="openTool('46')"
            >
                🖼️ 4×6 Photo Print
            </button>

            <button
                class="tool-btn"
                onclick="openTool('arranger')"
            >
                📑 PDF Arranger
            </button>

            <button
                class="tool-btn"
                onclick="openTool('topdf')"
            >
                📄 PDF, JPG, PNG to PDF
            </button>

            <button
                class="tool-btn"
                onclick="openTool('resize')"
            >
                📐 Image Resizer
            </button>

            <button
                class="tool-btn"
                onclick="openTool('pdfjpg')"
            >
                🖼️ PDF to JPG
            </button>

            <button
                class="tool-btn"
                onclick="openTool('compress')"
            >
                🗜️ PDF Compressor
            </button>

            <button
                class="tool-btn"
                onclick="openTool('history')"
            >
                📁 30-Day History
            </button>

        </div>


        <div class="account-bar">

            <div class="validity">

                ⏳ Account Validity:

                <b>
                    ${user.daysLeft ?? 0}
                    Days Left
                </b>

            </div>

            <div>
                Welcome,
                <b>
                    ${escapeHTML(user.name)}
                </b>
            </div>

        </div>


        <div id="customerToolArea"></div>

    </div>

    `;

    openTool("id");
}


/* =========================================================
   TOOL ROUTER
========================================================= */

function openTool(tool){

    document
        .querySelectorAll(".tool-btn")
        .forEach(button =>
            button.classList.remove("active")
        );

    const area =
        document.getElementById(
            "customerToolArea"
        );

    if(tool === "id"){

        document
            .getElementById("tool-id")
            ?.classList.add("active");

        idCardTool(area);

        return;
    }

    if(tool === "passport"){

        passportTool(area);

        return;
    }

    if(tool === "46"){

        fourSixTool(area);

        return;
    }

    if(tool === "resize"){

        imageResizeTool(area);

        return;
    }

    if(tool === "topdf"){

        imageToPDFTool(area);

        return;
    }

    if(tool === "pdfjpg"){

        pdfTool(
            area,
            "PDF to JPG"
        );

        return;
    }

    if(tool === "compress"){

        pdfTool(
            area,
            "PDF Compressor"
        );

        return;
    }

    if(tool === "arranger"){

        pdfTool(
            area,
            "PDF Arranger"
        );

        return;
    }

    if(tool === "name"){

        passportTool(
            area,
            "Name & Date Passport"
        );

        return;
    }

    if(tool === "history"){

        historyTool(area);

        return;
    }
}


/* =========================================================
   ID CARD
========================================================= */

function idCardTool(area){

    area.innerHTML = `

    <div class="hero">

        <span class="pill">
            AUTO-DIMENSION • SMART CROP •
            1013×638 • 2.5MM GAP • 5 CARDS
        </span>

        <h1>
            Card Generator System
        </h1>

        <p>
            Upload front and back ID images.
            System will fit them to standard ID size.
        </p>

    </div>


    <div class="grid">

        <div class="card">

            <h3>
                Front Side
            </h3>

            <div class="drop-zone">

                <input
                    id="frontImage"
                    type="file"
                    accept="image/*"
                >

                <img
                    id="frontPreview"
                    class="preview"
                >

            </div>

        </div>


        <div class="card">

            <h3>
                Back Side
            </h3>

            <div class="drop-zone">

                <input
                    id="backImage"
                    type="file"
                    accept="image/*"
                >

                <img
                    id="backPreview"
                    class="preview"
                >

            </div>

        </div>

    </div>


    <div class="card" style="margin-top:20px">

        <div class="hero">

            <span class="pill">
                1013 × 638 PX
            </span>

            <h2>
                5-Slot Print Preview
            </h2>

        </div>

        <div
            id="idPrintSheet"
            class="print-sheet"
        ></div>

        <div class="actions">

            <button
                class="btn btn-primary"
                onclick="generateIDCard()"
            >
                Generate ID Card
            </button>

        </div>

    </div>

    `;


    document
        .getElementById("frontImage")
        .addEventListener(
            "change",
            function(){

                previewFile(
                    this,
                    "frontPreview"
                );

                updateIDPreview();
            }
        );


    document
        .getElementById("backImage")
        .addEventListener(
            "change",
            function(){

                previewFile(
                    this,
                    "backPreview"
                );

            }
        );


    updateIDPreview();
}


function previewFile(input,id){

    const file =
        input.files[0];

    if(!file)return;

    document.getElementById(id).src =
        URL.createObjectURL(file);
}


function updateIDPreview(){

    const sheet =
        document.getElementById(
            "idPrintSheet"
        );

    if(!sheet)return;

    const front =
        document.getElementById(
            "frontPreview"
        )?.src;

    sheet.innerHTML = "";

    for(let i=0;i<5;i++){

        const card =
            document.createElement("div");

        card.className =
            "id-card";

        if(front){

            const img =
                document.createElement("img");

            img.src = front;

            card.appendChild(img);
        }

        sheet.appendChild(card);
    }
}


async function generateIDCard(){

    const input =
        document.getElementById(
            "frontImage"
        );

    if(!input.files.length){

        alert(
            "Please select Front Side image."
        );

        return;
    }

    const file =
        input.files[0];

    const form =
        new FormData();

    form.append(
        "file",
        file
    );

    form.append(
        "tool",
        "ID Card"
    );

    form.append(
        "width",
        "1013"
    );

    form.append(
        "height",
        "638"
    );

    form.append(
        "quality",
        "92"
    );

    try{

        const response =
            await fetch(
                "/api/process/image",
                {
                    method:"POST",
                    body:form
                }
            );

        if(!response.ok){

            const error =
                await response.json();

            throw new Error(
                error.error ||
                "Processing failed"
            );
        }

        const blob =
            await response.blob();

        downloadBlob(
            blob,
            "ID-Card-1013x638.jpg"
        );

    }catch(error){

        alert(error.message);
    }
}


/* =========================================================
   PASSPORT PHOTO
========================================================= */

function passportTool(
    area,
    customTitle="Passport Photos"
){

    area.innerHTML = `

    <div class="hero">

        <span class="pill">
            35 × 45 MM • 300 DPI •
            413 × 531 PX
        </span>

        <h1>
            ${customTitle}
        </h1>

        <p>
            Indian standard passport photo:
            35 mm × 45 mm.
        </p>

    </div>


    <div class="grid">

        <div class="card">

            <div class="drop-zone">

                <b>
                    Select Photo
                </b>

                <input
                    id="passportFile"
                    type="file"
                    accept="image/*"
                    style="margin-top:15px"
                >

            </div>

            <div class="controls">

                <div class="field">

                    <label>
                        Width
                    </label>

                    <input
                        id="passportWidth"
                        value="413"
                        type="number"
                    >

                </div>

                <div class="field">

                    <label>
                        Height
                    </label>

                    <input
                        id="passportHeight"
                        value="531"
                        type="number"
                    >

                </div>

                <div class="field">

                    <label>
                        DPI
                    </label>

                    <input
                        value="300"
                        disabled
                    >

                </div>

            </div>

            <div class="actions">

                <button
                    class="btn btn-primary"
                    onclick="processPassport()"
                >
                    Generate Passport Photo
                </button>

            </div>

        </div>


        <div class="card">

            <h3>
                Preview
            </h3>

            <img
                id="passportPreview"
                class="preview"
            >

        </div>

    </div>

    `;


    document
        .getElementById("passportFile")
        .addEventListener(
            "change",
            function(){

                previewFile(
                    this,
                    "passportPreview"
                );

            }
        );
}


async function processPassport(){

    const input =
        document.getElementById(
            "passportFile"
        );

    if(!input.files.length){

        alert(
            "Please select photo."
        );

        return;
    }

    await processImage(
        input.files[0],
        "Passport Photos",
        document.getElementById(
            "passportWidth"
        ).value,
        document.getElementById(
            "passportHeight"
        ).value
    );
}


/* =========================================================
   4x6 PHOTO
========================================================= */

function fourSixTool(area){

    area.innerHTML = `

    <div class="hero">

        <span class="pill">
            4 × 6 INCH • 300 DPI •
            1200 × 1800 PX
        </span>

        <h1>
            4×6 Photo Print
        </h1>

        <p>
            Standard 4×6 inch photo
            10.16 × 15.24 cm.
        </p>

    </div>


    <div class="grid">

        <div class="card">

            <div class="drop-zone">

                <b>
                    Choose Photo
                </b>

                <input
                    id="fourSixFile"
                    type="file"
                    accept="image/*"
                    style="margin-top:15px"
                >

            </div>

            <div class="controls">

                <div class="field">

                    <label>
                        Width
                    </label>

                    <input
                        id="fourSixWidth"
                        value="1200"
                        type="number"
                    >

                </div>

                <div class="field">

                    <label>
                        Height
                    </label>

                    <input
                        id="fourSixHeight"
                        value="1800"
                        type="number"
                    >

                </div>

                <div class="field">

                    <label>
                        DPI
                    </label>

                    <input
                        value="300"
                        disabled
                    >

                </div>

            </div>

            <div class="actions">

                <button
                    class="btn btn-primary"
                    onclick="process46()"
                >
                    Generate 4×6
                </button>

            </div>

        </div>


        <div class="card">

            <h3>
                Preview
            </h3>

            <img
                id="fourSixPreview"
                class="preview"
            >

        </div>

    </div>

    `;


    document
        .getElementById("fourSixFile")
        .addEventListener(
            "change",
            function(){

                previewFile(
                    this,
                    "fourSixPreview"
                );

            }
        );
}


async function process46(){

    const input =
        document.getElementById(
            "fourSixFile"
        );

    if(!input.files.length){

        alert(
            "Please select photo."
        );

        return;
    }

    await processImage(
        input.files[0],
        "4x6 Photo Print",
        1200,
        1800
    );
}


/* =========================================================
   GENERIC IMAGE PROCESSOR
========================================================= */

async function processImage(
    file,
    tool,
    width,
    height
){

    const form =
        new FormData();

    form.append(
        "file",
        file
    );

    form.append(
        "tool",
        tool
    );

    form.append(
        "width",
        width
    );

    form.append(
        "height",
        height
    );

    form.append(
        "quality",
        "92"
    );

    try{

        const response =
            await fetch(
                "/api/process/image",
                {
                    method:"POST",
                    body:form
                }
            );

        if(!response.ok){

            const data =
                await response.json();

            throw new Error(
                data.error ||
                "Processing failed"
            );
        }

        const blob =
            await response.blob();

        downloadBlob(
            blob,
            tool.replace(/\s+/g,"-") +
            ".jpg"
        );

    }catch(error){

        alert(error.message);
    }
}


/* =========================================================
   IMAGE RESIZER
========================================================= */

function imageResizeTool(area){

    area.innerHTML = `

    <div class="hero">

        <span class="pill">
            CUSTOM DIMENSIONS
        </span>

        <h1>
            Image Resizer
        </h1>

    </div>


    <div class="card">

        <div class="drop-zone">

            <input
                id="resizeFile"
                type="file"
                accept="image/*"
            >

        </div>


        <div class="controls">

            <div class="field">

                <label>
                    Width PX
                </label>

                <input
                    id="resizeWidth"
                    value="800"
                    type="number"
                >

            </div>

            <div class="field">

                <label>
                    Height PX
                </label>

                <input
                    id="resizeHeight"
                    value="800"
                    type="number"
                >

            </div>

            <div class="field">

                <label>
                    Quality
                </label>

                <input
                    id="resizeQuality"
                    value="90"
                    type="number"
                    min="1"
                    max="100"
                >

            </div>

        </div>


        <div class="actions">

            <button
                class="btn btn-primary"
                onclick="resizeImage()"
            >
                Resize & Download
            </button>

        </div>

    </div>

    `;
}


async function resizeImage(){

    const file =
        document.getElementById(
            "resizeFile"
        ).files[0];

    if(!file){

        alert(
            "Choose an image."
        );

        return;
    }

    await processImage(
        file,
        "Image Resizer",
        document.getElementById(
            "resizeWidth"
        ).value,
        document.getElementById(
            "resizeHeight"
        ).value
    );
}


/* =========================================================
   JPG PNG TO PDF
========================================================= */

function imageToPDFTool(area){

    area.innerHTML = `

    <div class="hero">

        <span class="pill">
            JPG • PNG → PDF
        </span>

        <h1>
            PDF Converter
        </h1>

        <p>
            Select multiple images.
            They will become PDF pages.
        </p>

    </div>


    <div class="card">

        <input
            id="pdfImages"
            type="file"
            accept="image/jpeg,image/png"
            multiple
        >

        <div class="actions">

            <button
                class="btn btn-primary"
                onclick="createPDF()"
            >
                Create PDF
            </button>

        </div>

    </div>

    `;
}


async function createPDF(){

    const files =
        [
            ...document.getElementById(
                "pdfImages"
            ).files
        ];

    if(!files.length){

        alert(
            "Select images."
        );

        return;
    }

    const form =
        new FormData();

    files.forEach(
        file =>
            form.append(
                "files",
                file
            )
    );

    try{

        const response =
            await fetch(
                "/api/process/images-to-pdf",
                {
                    method:"POST",
                    body:form
                }
            );

        if(!response.ok){

            const data =
                await response.json();

            throw new Error(
                data.error
            );
        }

        const blob =
            await response.blob();

        downloadBlob(
            blob,
            "converted.pdf"
        );

    }catch(error){

        alert(error.message);
    }
}


/* =========================================================
   PDF TOOLS
========================================================= */

function pdfTool(area,title){

    area.innerHTML = `

    <div class="hero">

        <span class="pill">
            PDF PROCESSING
        </span>

        <h1>
            ${title}
        </h1>

    </div>


    <div class="card">

        <input
            id="pdfFile"
            type="file"
            accept="application/pdf"
        >


        <div class="controls">

            <div class="field">

                <label>
                    DPI
                </label>

                <select id="pdfDPI">

                    <option>
                        72
                    </option>

                    <option>
                        96
                    </option>

                    <option>
                        150
                    </option>

                    <option>
                        200
                    </option>

                    <option selected>
                        300
                    </option>

                    <option>
                        600
                    </option>

                </select>

            </div>

        </div>


        <div class="actions">

            <button
                class="btn btn-primary"
                onclick="analyzePDF('${title}')"
            >
                Analyze PDF
            </button>

        </div>


        <div
            id="pdfResult"
            style="margin-top:20px"
        ></div>

    </div>

    `;
}


async function analyzePDF(tool){

    const file =
        document.getElementById(
            "pdfFile"
        ).files[0];

    if(!file){

        alert(
            "Choose PDF."
        );

        return;
    }

    const form =
        new FormData();

    form.append(
        "file",
        file
    );

    form.append(
        "tool",
        tool
    );

    form.append(
        "dpi",
        document.getElementById(
            "pdfDPI"
        ).value
    );

    try{

        const response =
            await fetch(
                "/api/process/pdf-info",
                {
                    method:"POST",
                    body:form
                }
            );

        const data =
            await response.json();

        if(!response.ok){

            throw new Error(
                data.error
            );
        }

        document.getElementById(
            "pdfResult"
        ).innerHTML = `

            <div class="note">
                Total Pages:
                ${data.pages}
            </div>

            ${
                data.dimensions
                    .map(page => `

                    <div class="history-row">

                        <span>
                            Page ${page.page}
                        </span>

                        <span>
                            ${page.width.toFixed(1)}
                            ×
                            ${page.height.toFixed(1)}
                            pt
                        </span>

                    </div>

                    `)
                    .join("")
            }

        `;

    }catch(error){

        alert(error.message);
    }
}


/* =========================================================
   30 DAY HISTORY
========================================================= */

async function historyTool(area){

    try{

        const history =
            await api(
                "/api/history"
            );

        area.innerHTML = `

        <div class="hero">

            <span class="pill">
                SERVER-SIDE • 30 DAYS
            </span>

            <h1>
                30-Day History
            </h1>

            <p>
                History is stored on the server,
                not browser localStorage.
            </p>

        </div>


        <div class="card">

            ${
                history.length

                ?

                history.map(item => `

                    <div class="history-row">

                        <div>

                            <b>
                                ${escapeHTML(
                                    item.tool
                                )}
                            </b>

                            <br>

                            <span class="note">
                                ${escapeHTML(
                                    item.file_name
                                )}
                            </span>

                        </div>

                        <div>

                            ${new Date(
                                item.created_at
                            ).toLocaleString()}

                            <br>

                            <span class="note">
                                ${escapeHTML(
                                    item.status
                                )}
                            </span>

                        </div>

                    </div>

                `).join("")

                :

                `
                <div class="note">
                    No history available.
                </div>
                `
            }

        </div>

        `;

    }catch(error){

        area.innerHTML = `

        <div class="card">

            <p>
                Unable to load history.
            </p>

            <small>
                Backend connection required.
            </small>

        </div>

        `;
    }
}


/* =========================================================
   ADMIN DASHBOARD
========================================================= */

async function showAdmin(){

    document.getElementById("app").innerHTML = `

    <div class="admin-layout">

        <aside class="admin-sidebar">

            <h2>
                ID Card Printing
            </h2>

            <button
                class="btn btn-primary"
                onclick="adminPage('dashboard')"
            >
                Dashboard
            </button>

            <button
                class="btn"
                onclick="adminPage('customers')"
            >
                Customers
            </button>

            <button
                class="btn"
                onclick="adminPage('payments')"
            >
                Payments
            </button>

            <button
                class="btn"
                onclick="logout()"
            >
                Logout
            </button>

        </aside>


        <main class="admin-main">

            <div id="adminContent"></div>

        </main>

    </div>

    `;

    adminPage("dashboard");
}


/* =========================================================
   ADMIN PAGES
========================================================= */

async function adminPage(page){

    const area =
        document.getElementById(
            "adminContent"
        );

    if(page === "dashboard"){

        const customers =
            await api(
                "/api/admin/customers"
            );

        const active =
            customers.filter(
                c => c.active
            ).length;

        const pending =
            customers.reduce(
                (sum,c) =>
                    sum + Number(
                        c.pending || 0
                    ),
                0
            );

        area.innerHTML = `

        <h1>
            Admin Dashboard
        </h1>

        <p class="note">
            Customer and payment management
        </p>


        <div class="stats">

            <div class="stat">

                <small>
                    Total Customers
                </small>

                <strong>
                    ${customers.length}
                </strong>

            </div>


            <div class="stat">

                <small>
                    Active Customers
                </small>

                <strong>
                    ${active}
                </strong>

            </div>


            <div class="stat">

                <small>
                    Pending Payments
                </small>

                <strong>
                    ₹${pending.toLocaleString(
                        "en-IN"
                    )}
                </strong>

            </div>


            <div class="stat">

                <small>
                    History
                </small>

                <strong>
                    30 Days
                </strong>

            </div>

        </div>

        `;

        return;
    }


    if(page === "customers"){

        const customers =
            await api(
                "/api/admin/customers"
            );

        area.innerHTML = `

        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            gap:15px;
        ">

            <div>

                <h1>
                    Customers
                </h1>

                <p class="note">
                    Accounts can only be created by Admin.
                </p>

            </div>

            <button
                class="btn btn-primary"
                onclick="createCustomer()"
            >
                + Create Customer
            </button>

        </div>


        <div
            class="card"
            style="margin-top:20px"
        >

            <div class="table-wrapper">

                <table class="table">

                    <thead>

                        <tr>

                            <th>
                                Name
                            </th>

                            <th>
                                Username
                            </th>

                            <th>
                                Mobile
                            </th>

                            <th>
                                Status
                            </th>

                            <th>
                                Validity
                            </th>

                            <th>
                                Action
                            </th>

                        </tr>

                    </thead>

                    <tbody>

                    ${
                        customers.map(c => `

                        <tr>

                            <td>
                                ${escapeHTML(
                                    c.name
                                )}
                            </td>

                            <td>
                                ${escapeHTML(
                                    c.username
                                )}
                            </td>

                            <td>
                                ${escapeHTML(
                                    c.mobile
                                )}
                            </td>

                            <td>

                                <span
                                    class="badge
                                    ${
                                        c.active
                                        ? "badge-active"
                                        : "badge-inactive"
                                    }"
                                >

                                    ${
                                        c.active
                                        ? "Active"
                                        : "Inactive"
                                    }

                                </span>

                            </td>

                            <td>
                                ${c.daysLeft}
                                Days
                            </td>

                            <td>

                                <button
                                    class="btn"
                                    onclick="
                                        toggleCustomer(
                                            ${c.id},
                                            ${!c.active}
                                        )
                                    "
                                >

                                    ${
                                        c.active
                                        ? "Disable"
                                        : "Enable"
                                    }

                                </button>

                            </td>

                        </tr>

                        `).join("")
                    }

                    </tbody>

                </table>

            </div>

        </div>

        `;

        return;
    }


    if(page === "payments"){

        const payments =
            await api(
                "/api/admin/payments"
            );

        area.innerHTML = `

        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
        ">

            <div>

                <h1>
                    Payments
                </h1>

                <p class="note">
                    Customer payment management
                </p>

            </div>

            <button
                class="btn btn-primary"
                onclick="recordPayment()"
            >
                + Record Payment
            </button>

        </div>


        <div
            class="card"
            style="margin-top:20px"
        >

            <div class="table-wrapper">

                <table class="table">

                    <thead>

                        <tr>

                            <th>
                                Customer
                            </th>

                            <th>
                                Amount
                            </th>

                            <th>
                                Status
                            </th>

                            <th>
                                Date
                            </th>

                        </tr>

                    </thead>

                    <tbody>

                    ${
                        payments.map(p => `

                        <tr>

                            <td>
                                ${escapeHTML(
                                    p.name
                                )}
                                <br>
                                <small>
                                    ${escapeHTML(
                                        p.username
                                    )}
                                </small>
                            </td>

                            <td>
                                ₹${Number(
                                    p.amount
                                ).toLocaleString(
                                    "en-IN"
                                )}
                            </td>

                            <td>
                                ${escapeHTML(
                                    p.status
                                )}
                            </td>

                            <td>
                                ${
                                    p.created_at
                                    ?
                                    new Date(
                                        p.created_at
                                    ).toLocaleString()
                                    :
                                    "-"
                                }
                            </td>

                        </tr>

                        `).join("")
                    }

                    </tbody>

                </table>

            </div>

        </div>

        `;
    }
}


/* =========================================================
   CREATE CUSTOMER
========================================================= */

async function createCustomer(){

    const name =
        prompt(
            "Customer Name:"
        );

    if(!name)return;

    const username =
        prompt(
            "Customer Username:"
        );

    if(!username)return;

    const password =
        prompt(
            "Customer Password:"
        );

    if(!password)return;

    const mobile =
        prompt(
            "Mobile Number:"
        ) || "";

    const email =
        prompt(
            "Email:"
        ) || "";

    const validity =
        prompt(
            "Validity in Days:",
            "365"
        ) || "365";

    try{

        const result =
            await api(
                "/api/admin/customers",
                {
                    method:"POST",

                    body:JSON.stringify({

                        name,

                        username,

                        password,

                        mobile,

                        email,

                        validityDays:
                            Number(
                                validity
                            )

                    })
                }
            );

        alert(
            "Customer account created successfully.\n\n" +
            "Username: " +
            result.username +
            "\nExpiry: " +
            new Date(
                result.expiresAt
            ).toLocaleDateString()
        );

        adminPage("customers");

    }catch(error){

        alert(error.message);
    }
}


/* =========================================================
   CUSTOMER ACTIVE / INACTIVE
========================================================= */

async function toggleCustomer(
    id,
    active
){

    try{

        await api(
            "/api/admin/customers/" +
            id,
            {
                method:"PATCH",

                body:JSON.stringify({
                    active
                })
            }
        );

        adminPage("customers");

    }catch(error){

        alert(error.message);
    }
}


/* =========================================================
   PAYMENT
========================================================= */

async function recordPayment(){

    const customers =
        await api(
            "/api/admin/customers"
        );

    const list =
        customers
            .map(
                c =>
                `${c.id}: ${c.name} (${c.username})`
            )
            .join("\n");

    const customerId =
        prompt(
            "Customer ID:\n\n" +
            list
        );

    if(!customerId)return;

    const amount =
        prompt(
            "Payment Amount:"
        );

    if(!amount)return;

    try{

        await api(
            "/api/admin/payments",
            {
                method:"POST",

                body:JSON.stringify({

                    customerId:
                        Number(
                            customerId
                        ),

                    amount:
                        Number(
                            amount
                        ),

                    status:"Paid"

                })
            }
        );

        alert(
            "Payment recorded."
        );

        adminPage("payments");

    }catch(error){

        alert(error.message);
    }
}


/* =========================================================
   DOWNLOAD
========================================================= */

function downloadBlob(
    blob,
    filename
){

    const url =
        URL.createObjectURL(
            blob
        );

    const a =
        document.createElement(
            "a"
        );

    a.href = url;

    a.download =
        filename;

    document.body.appendChild(a);

    a.click();

    a.remove();

    setTimeout(
        () =>
            URL.revokeObjectURL(
                url
            ),
        1000
    );
}


/* =========================================================
   START APP
========================================================= */

start();

</script>

</body>
</html>
