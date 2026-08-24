<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>ID Card Printing Portal</title>

<style>
:root{
    --bg:#08070d;
    --panel:#111019;
    --panel2:#171521;
    --panel3:#1c1928;
    --line:#302b3d;
    --text:#f8f6fb;
    --muted:#aaa4b5;

    --primary:#806cff;
    --primary2:#a07cff;
    --pink:#f05bd5;

    --green:#55d99a;
    --red:#ff687c;
    --yellow:#ffc857;
    --blue:#62b5ff;
}

*{
    box-sizing:border-box;
}

html{
    scroll-behavior:smooth;
}

body{
    margin:0;
    min-height:100vh;

    color:var(--text);

    font-family:
        Inter,
        ui-sans-serif,
        system-ui,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;

    background:
        radial-gradient(
            circle at 50% -10%,
            rgba(122,77,180,.35),
            transparent 38%
        ),
        radial-gradient(
            circle at 100% 20%,
            rgba(74,55,170,.16),
            transparent 30%
        ),
        #08070d;
}

button,
input,
select{
    font:inherit;
}

button{
    cursor:pointer;
}

img{
    max-width:100%;
}

.hidden{
    display:none!important;
}


/* =========================================================
   GLOBAL
========================================================= */

.container{
    width:100%;
    max-width:1500px;
    margin:auto;
    padding:20px;
}

.btn{
    min-width:140px;
    height:46px;

    padding:0 18px;

    border-radius:12px;

    border:1px solid var(--line);

    color:white;

    background:#171520;

    transition:
        .2s ease;
}

.btn:hover{
    transform:translateY(-1px);
    border-color:#8072ff;
    box-shadow:
        0 8px 25px rgba(0,0,0,.25);
}

.btn-primary{
    background:
        linear-gradient(
            135deg,
            #6d5cff,
            #9b6cff
        );

    border-color:#9b8fff;
}

.btn-success{
    background:
        linear-gradient(
            135deg,
            #248b61,
            #35bb80
        );

    border-color:#62dba3;
}

.btn-danger{
    background:#3c1c25;
    border-color:#6b303c;
}

.btn-small{
    min-width:auto;
    height:38px;
    padding:0 13px;
}

.badge{
    display:inline-flex;
    align-items:center;

    min-height:28px;

    padding:0 10px;

    border-radius:20px;

    font-size:12px;
    font-weight:700;
}

.badge-green{
    color:#86edb7;
    background:#11291f;
    border:1px solid #275d44;
}

.badge-blue{
    color:#92d1ff;
    background:#112433;
    border:1px solid #2b5a78;
}

.badge-yellow{
    color:#ffd76c;
    background:#302714;
    border:1px solid #67532a;
}


/* =========================================================
   LOGIN
========================================================= */

.login-page{
    min-height:100vh;

    display:flex;
    align-items:center;
    justify-content:center;

    padding:20px;
}

.login-box{
    width:440px;
    max-width:100%;

    padding:34px;

    background:
        linear-gradient(
            145deg,
            rgba(25,22,36,.98),
            rgba(13,12,19,.98)
        );

    border:1px solid #393247;

    border-radius:24px;

    box-shadow:
        0 35px 100px rgba(0,0,0,.65);
}

.login-logo{
    text-align:center;

    font-size:27px;
    font-weight:900;

    letter-spacing:.5px;

    background:
        linear-gradient(
            90deg,
            #aa8bff,
            #ff61d3
        );

    -webkit-background-clip:text;
    background-clip:text;

    color:transparent;
}

.login-subtitle{
    text-align:center;

    color:var(--muted);

    margin-top:8px;
    margin-bottom:28px;
}

.field{
    margin:15px 0;
}

.field label{
    display:block;

    color:#bbb5c5;

    font-size:12px;
    font-weight:600;

    margin-bottom:7px;
}

.field input,
.field select{

    width:100%;

    height:44px;

    padding:0 12px;

    color:white;

    background:#0c0b12;

    border:1px solid #302b3b;

    border-radius:10px;

    outline:none;
}

.field input:focus,
.field select:focus{
    border-color:#8072ff;
    box-shadow:
        0 0 0 3px rgba(128,108,255,.12);
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
    min-height:20px;

    text-align:center;

    color:var(--red);

    font-size:13px;

    margin-top:12px;
}


/* =========================================================
   TOPBAR
========================================================= */

.topbar{

    display:flex;

    justify-content:space-between;
    align-items:center;

    gap:20px;

    padding:12px 0 18px;

    border-bottom:1px solid #443b4c;
}

.logo{
    font-size:24px;
    font-weight:900;

    letter-spacing:.5px;

    background:
        linear-gradient(
            90deg,
            #b18cff,
            #ff5bd5
        );

    -webkit-background-clip:text;
    background-clip:text;

    color:transparent;
}

.top-actions{
    display:flex;
    gap:8px;
}


/* =========================================================
   TOOL NAV
========================================================= */

.tool-bar{

    display:flex;

    flex-wrap:wrap;

    justify-content:center;

    gap:9px;

    padding:20px 0;
}

.tool-btn{

    min-width:145px;
    height:44px;

    padding:0 14px;

    color:white;

    background:#15131e;

    border:1px solid #312c3d;

    border-radius:11px;

    font-size:12px;
    font-weight:700;

    transition:.2s;
}

.tool-btn:hover{
    border-color:#7e70ff;
}

.tool-btn.active{

    background:
        linear-gradient(
            135deg,
            #5f72ff,
            #8064ff
        );

    border-color:#9a92ff;

    box-shadow:
        0 7px 22px rgba(91,77,255,.2);
}


/* =========================================================
   ACCOUNT
========================================================= */

.account-bar{

    display:flex;

    align-items:center;
    justify-content:space-between;

    gap:15px;

    padding:15px 18px;

    background:#121019;

    border:1px solid #3a3445;

    border-radius:17px;
}

.validity{

    padding:9px 15px;

    border-radius:20px;

    color:#9eeeb9;

    background:#112119;

    border:1px solid #285d43;

    font-size:13px;
}

.validity b{
    color:#ffd05d;
}


/* =========================================================
   HERO
========================================================= */

.hero{
    text-align:center;

    padding:30px 10px 24px;
}

.hero h1{

    margin:13px 0 8px;

    font-size:36px;

    background:
        linear-gradient(
            90deg,
            #b38aff,
            #ff62d3
        );

    -webkit-background-clip:text;
    background-clip:text;

    color:transparent;
}

.hero p{
    margin:0;

    color:var(--muted);
}

.pill{

    display:inline-flex;

    align-items:center;

    padding:8px 15px;

    border-radius:20px;

    color:#a8d9ff;

    background:#122332;

    border:1px solid #315d7b;

    font-size:11px;

    font-weight:800;

    letter-spacing:.3px;
}


/* =========================================================
   CARDS
========================================================= */

.grid{

    display:grid;

    grid-template-columns:
        repeat(2,minmax(0,1fr));

    gap:18px;
}

.card{

    background:
        linear-gradient(
            145deg,
            #14121c,
            #0f0e15
        );

    border:1px solid #302b3b;

    border-radius:17px;

    padding:20px;
}

.card-title{
    margin-top:0;
}


/* =========================================================
   UPLOAD
========================================================= */

.drop-zone{

    min-height:170px;

    display:flex;

    align-items:center;
    justify-content:center;

    flex-direction:column;

    gap:12px;

    text-align:center;

    border:2px dashed #55566b;

    border-radius:15px;

    background:#0c0b12;
}

.drop-zone:hover{
    border-color:#8277ff;
}

.file-input{

    width:100%;

    color:#aaa5b3;
}


/* =========================================================
   DIMENSION PANEL
========================================================= */

.dimension-panel{

    display:grid;

    grid-template-columns:
        1.4fr 1fr 1fr 1fr;

    gap:10px;

    margin-top:16px;
}

.dimension-info{

    margin-top:12px;

    padding:12px;

    border-radius:10px;

    background:#0d0c13;

    border:1px solid #292532;

    color:#aaa5b3;

    font-size:12px;
}

.dimension-info strong{
    color:white;
}


/* =========================================================
   PREVIEW
========================================================= */

.preview-layout{

    display:grid;

    grid-template-columns:
        minmax(0,1fr)
        minmax(0,1fr);

    gap:18px;

    margin-top:18px;
}

.preview-box{

    min-height:280px;

    display:flex;

    align-items:center;
    justify-content:center;

    flex-direction:column;

    gap:12px;

    padding:18px;

    background:#09080d;

    border:1px solid #302b3b;

    border-radius:14px;
}

.preview-box img{

    max-width:100%;
    max-height:400px;

    object-fit:contain;

    border-radius:8px;
}

.preview-label{

    width:100%;

    color:#aaa5b3;

    font-size:12px;
}


/* =========================================================
   ACTIONS
========================================================= */

.actions{

    display:flex;

    flex-wrap:wrap;

    justify-content:flex-end;

    gap:10px;

    margin-top:18px;
}

.download-row{

    display:flex;

    flex-wrap:wrap;

    justify-content:center;

    gap:12px;

    margin-top:18px;
}


/* =========================================================
   PRINT SHEET
========================================================= */

.print-preview-wrapper{

    overflow:auto;

    padding:15px;

    background:#050509;

    border-radius:14px;

    border:1px solid #2d2937;
}

.a4-sheet{

    width:794px;
    min-height:1123px;

    margin:auto;

    background:white;

    color:#000;

    padding:35px;

    box-shadow:
        0 15px 60px rgba(0,0,0,.45);

    display:grid;

    grid-template-columns:
        repeat(2,1fr);

    align-content:start;

    gap:20px;
}

.a4-sheet.photo-4x6{

    grid-template-columns:
        repeat(2,1fr);

    gap:15px;
}

.a4-photo{

    width:100%;

    aspect-ratio:4/6;

    object-fit:cover;

    border:1px solid #ddd;
}

.a4-passport{

    width:138px;
    height:177px;

    object-fit:cover;

    border:1px solid #bbb;
}

.a4-id{

    width:100%;

    aspect-ratio:1013/638;

    object-fit:cover;

    border:2px solid #000;
}


/* =========================================================
   ID CARD
========================================================= */

.id-card-preview{

    width:min(100%,650px);

    aspect-ratio:1013/638;

    background:#eee;

    border:4px solid #000;

    overflow:hidden;

    border-radius:6px;

    margin:auto;
}

.id-card-preview img{

    width:100%;
    height:100%;

    object-fit:cover;
}

.id-sheet{

    display:grid;

    grid-template-columns:
        repeat(2,1fr);

    gap:15px;
}

.id-slot{

    aspect-ratio:1013/638;

    background:#eee;

    border:2px solid #000;

    overflow:hidden;
}

.id-slot img{

    width:100%;
    height:100%;

    object-fit:cover;
}


/* =========================================================
   HISTORY
========================================================= */

.history-row{

    display:flex;

    justify-content:space-between;

    gap:20px;

    padding:14px 0;

    border-bottom:1px solid #292531;
}

.note{
    color:var(--muted);
    font-size:12px;
}


/* =========================================================
   ADMIN
========================================================= */

.admin-layout{

    min-height:100vh;

    display:grid;

    grid-template-columns:235px 1fr;
}

.admin-sidebar{

    padding:18px;

    background:#0c0b11;

    border-right:1px solid #302b3b;
}

.admin-sidebar h2{

    font-size:18px;

    margin:5px 0 20px;
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

    grid-template-columns:
        repeat(4,1fr);

    gap:12px;
}

.stat{

    padding:18px;

    background:#121019;

    border:1px solid #302b3b;

    border-radius:15px;
}

.stat small{
    color:var(--muted);
}

.stat strong{

    display:block;

    margin-top:7px;

    font-size:26px;
}


/* =========================================================
   TABLE
========================================================= */

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

    padding:12px;

    text-align:left;

    border-bottom:1px solid #2b2733;
}

.table th{
    color:#aaa4b5;
    font-size:12px;
}


/* =========================================================
   RESPONSIVE
========================================================= */

@media(max-width:1000px){

    .grid,
    .preview-layout{

        grid-template-columns:1fr;
    }

    .dimension-panel{

        grid-template-columns:
            repeat(2,1fr);
    }

    .stats{

        grid-template-columns:
            repeat(2,1fr);
    }

    .admin-layout{

        grid-template-columns:1fr;
    }

    .admin-sidebar{

        border-right:none;
        border-bottom:1px solid #302b3b;
    }
}

@media(max-width:650px){

    .container{
        padding:12px;
    }

    .topbar{

        align-items:flex-start;

        flex-direction:column;
    }

    .account-bar{

        flex-direction:column;

        align-items:flex-start;
    }

    .tool-btn{

        flex:1 1 calc(50% - 10px);

        min-width:0;
    }

    .dimension-panel{

        grid-template-columns:1fr;
    }

    .stats{

        grid-template-columns:1fr;
    }

    .a4-sheet{

        transform-origin:top left;

        width:700px;
    }

    .actions,
    .download-row{

        justify-content:center;
    }

    .btn{

        width:100%;
    }
}
</style>
</head>


<body>

<div id="app"></div>


<script>

/* =========================================================
   GLOBAL DIMENSIONS
========================================================= */

const DIMENSIONS = {

    idCard:{
        name:"Standard ID Card",
        width:1013,
        height:638,
        unit:"px",
        dpi:300,
        ratio:"1013:638"
    },

    passport:{
        name:"Indian Passport Photo",
        width:413,
        height:531,
        unit:"px",
        mmWidth:35,
        mmHeight:45,
        dpi:300,
        ratio:"7:9"
    },

    photo4x6:{
        name:"4×6 Photo",
        width:1200,
        height:1800,
        unit:"px",
        inchWidth:4,
        inchHeight:6,
        dpi:300,
        ratio:"2:3"
    },

    a4:{
        name:"A4",
        width:2480,
        height:3508,
        unit:"px",
        mmWidth:210,
        mmHeight:297,
        dpi:300,
        ratio:"1:1.414"
    },

    a5:{
        name:"A5",
        width:1748,
        height:2480,
        unit:"px",
        mmWidth:148,
        mmHeight:210,
        dpi:300
    },

    a3:{
        name:"A3",
        width:3508,
        height:4961,
        unit:"px",
        mmWidth:297,
        mmHeight:420,
        dpi:300
    },

    square2x2:{
        name:"2×2 Visa Photo",
        width:600,
        height:600,
        unit:"px",
        inchWidth:2,
        inchHeight:2,
        dpi:300,
        ratio:"1:1"
    },

    stamp:{
        name:"Stamp Photo",
        width:600,
        height:600,
        unit:"px",
        inchWidth:2,
        inchHeight:2,
        dpi:300,
        ratio:"1:1"
    }
};


/* =========================================================
   API
========================================================= */

async function api(url,options={}){

    const response =
        await fetch(
            url,
            {
                ...options,

                headers:
                    options.body instanceof FormData
                    ?
                    options.headers
                    :
                    {
                        "Content-Type":
                            "application/json",

                        ...(options.headers || {})
                    }
            }
        );

    const data =
        await response
            .json()
            .catch(
                () => ({})
            );

    if(!response.ok){

        throw new Error(
            data.error ||
            "Request failed"
        );
    }

    return data;
}


/* =========================================================
   ESCAPE
========================================================= */

function escapeHTML(value){

    return String(value ?? "")
        .replace(
            /[&<>"']/g,
            char => ({
                "&":"&amp;",
                "<":"&lt;",
                ">":"&gt;",
                '"':"&quot;",
                "'":"&#039;"
            }[char])
        );
}


/* =========================================================
   START
========================================================= */

async function start(){

    try{

        const user =
            await api(
                "/api/me"
            );

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

let loginType="customer";


function showLogin(){

    document.getElementById(
        "app"
    ).innerHTML = `

    <div class="login-page">

        <div class="login-box">

            <div class="login-logo">
                ID CARD PRINTING PORTAL
            </div>

            <div
                class="login-subtitle"
                id="loginSubtitle"
            >
                Customer Login
            </div>


            <div class="field">

                <label id="usernameLabel">
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
                    class="btn btn-small"
                    onclick="showHelp()"
                >
                    Help
                </button>

                <button
                    class="btn btn-small"
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

    loginType="admin";

    document.getElementById(
        "loginSubtitle"
    ).innerText =
        "Administrator Login";

    document.getElementById(
        "usernameLabel"
    ).innerText =
        "Admin Email";

    document.getElementById(
        "loginUsername"
    ).placeholder =
        "Enter admin email";
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

    error.innerText="";

    if(!username || !password){

        error.innerText =
            "Username and password required.";

        return;
    }

    try{

        const result =
            await api(
                "/api/login",
                {
                    method:"POST",

                    body:JSON.stringify({

                        type:loginType,

                        username,

                        password

                    })
                }
            );

        if(result.role==="admin"){

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
            await api(
                "/api/help"
            );

        alert(
            "HELP\n\n"+
            "Email: "+
            data.email+
            "\nMobile: "+
            data.mobile
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

    try{

        await api(
            "/api/logout",
            {
                method:"POST"
            }
        );

    }finally{

        start();
    }
}


/* =========================================================
   CUSTOMER
========================================================= */

function showCustomer(user){

    document.getElementById(
        "app"
    ).innerHTML = `

    <div class="container">


        <div class="topbar">

            <div class="logo">
                ID CARD PRINTING PORTAL
            </div>

            <div class="top-actions">

                <button
                    class="btn btn-small"
                    onclick="showHelp()"
                >
                    Help
                </button>

                <button
                    class="btn btn-small btn-danger"
                    onclick="logout()"
                >
                    Logout
                </button>

            </div>

        </div>


        <div class="tool-bar">

            <button
                class="tool-btn"
                onclick="openTool('id',this)"
            >
                🪪 ID Card
            </button>

            <button
                class="tool-btn"
                onclick="openTool('passport',this)"
            >
                👤 Passport Photo
            </button>

            <button
                class="tool-btn"
                onclick="openTool('passportName',this)"
            >
                📄 Name & Date
            </button>

            <button
                class="tool-btn"
                onclick="openTool('4x6',this)"
            >
                🖼️ 4×6 Photo
            </button>

            <button
                class="tool-btn"
                onclick="openTool('arranger',this)"
            >
                📑 PDF Arranger
            </button>

            <button
                class="tool-btn"
                onclick="openTool('topdf',this)"
            >
                📄 Images → PDF
            </button>

            <button
                class="tool-btn"
                onclick="openTool('resize',this)"
            >
                📐 Image Resize
            </button>

            <button
                class="tool-btn"
                onclick="openTool('pdfjpg',this)"
            >
                🖼️ PDF → JPG
            </button>

            <button
                class="tool-btn"
                onclick="openTool('compress',this)"
            >
                🗜️ PDF Compress
            </button>

            <button
                class="tool-btn"
                onclick="openTool('history',this)"
            >
                📁 History
            </button>

        </div>


        <div class="account-bar">

            <div class="validity">

                Account Validity:

                <b>
                    ${user.daysLeft ?? 0}
                    Days
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

    openTool(
        "id",
        document.querySelector(
            ".tool-btn"
        )
    );
}


/* =========================================================
   TOOL ROUTER
========================================================= */

function openTool(tool,button){

    document
        .querySelectorAll(
            ".tool-btn"
        )
        .forEach(
            b =>
                b.classList.remove(
                    "active"
                )
        );

    if(button){

        button.classList.add(
            "active"
        );
    }

    const area =
        document.getElementById(
            "customerToolArea"
        );


    switch(tool){

        case "id":
            idCardTool(area);
            break;

        case "passport":
            passportTool(area,false);
            break;

        case "passportName":
            passportTool(area,true);
            break;

        case "4x6":
            fourSixTool(area);
            break;

        case "resize":
            resizeTool(area);
            break;

        case "topdf":
            imagePDFTool(area);
            break;

        case "pdfjpg":
            pdfTool(
                area,
                "PDF to JPG"
            );
            break;

        case "compress":
            pdfTool(
                area,
                "PDF Compressor"
            );
            break;

        case "arranger":
            pdfTool(
                area,
                "PDF Arranger"
            );
            break;

        case "history":
            historyTool(area);
            break;
    }
}


/* =========================================================
   ID CARD TOOL
========================================================= */

function idCardTool(area){

    area.innerHTML = `

    <div class="hero">

        <span class="pill">
            1013 × 638 PX • 300 DPI •
            AUTO CROP • SMART FIT
        </span>

        <h1>
            ID Card Generator
        </h1>

        <p>
            Upload the ID image and preview the
            final 1013 × 638 card before downloading.
        </p>

    </div>


    <div class="card">

        <h3 class="card-title">
            Upload ID Card
        </h3>

        <div class="drop-zone">

            <input
                id="idFile"
                class="file-input"
                type="file"
                accept="image/*,application/pdf"
            >

            <span class="note">
                JPG / PNG / PDF
            </span>

        </div>


        <div class="dimension-info">

            Standard output:

            <strong>
                1013 × 638 px
            </strong>

            &nbsp; • &nbsp;

            300 DPI

            &nbsp; • &nbsp;

            Broad Black Border

        </div>

    </div>


    <div
        class="preview-layout"
        style="margin-top:18px"
    >

        <div class="card">

            <div class="preview-label">
                ORIGINAL PREVIEW
            </div>

            <div class="preview-box">

                <img
                    id="idOriginal"
                    alt=""
                >

                <span
                    id="idOriginalText"
                    class="note"
                >
                    Upload a file
                </span>

            </div>

        </div>


        <div class="card">

            <div class="preview-label">
                FINAL ID CARD PREVIEW
            </div>

            <div class="preview-box">

                <div
                    id="idFinal"
                    class="id-card-preview"
                ></div>

                <span class="note">
                    1013 × 638 px
                </span>

            </div>

        </div>

    </div>


    <div class="card" style="margin-top:18px">

        <h3>
            Print Sheet Preview
        </h3>

        <div class="print-preview-wrapper">

            <div
                id="idA4Preview"
                class="a4-sheet"
            ></div>

        </div>


        <div class="download-row">

            <button
                class="btn btn-primary"
                onclick="downloadID()"
            >
                Download ID Card
            </button>

            <button
                class="btn btn-success"
                onclick="downloadIDA4()"
            >
                Download in A4
            </button>

        </div>

    </div>

    `;


    document
        .getElementById("idFile")
        .addEventListener(
            "change",
            previewID
        );
}


function previewID(event){

    const file =
        event.target.files[0];

    if(!file)return;

    if(file.type.startsWith("image/")){

        const url =
            URL.createObjectURL(file);

        document.getElementById(
            "idOriginal"
        ).src=url;

        document.getElementById(
            "idOriginalText"
        ).innerText =
            file.name;

        const final =
            document.getElementById(
                "idFinal"
            );

        final.innerHTML = `

            <img
                src="${url}"
                alt=""
            >

        `;

        createIDA4Preview(url);
    }
}


function createIDA4Preview(url){

    const sheet =
        document.getElementById(
            "idA4Preview"
        );

    if(!sheet)return;

    sheet.innerHTML="";

    for(
        let i=0;
        i<10;
        i++
    ){

        sheet.innerHTML += `

            <div class="id-slot">

                <img
                    src="${url}"
                    alt=""
                >

            </div>

        `;
    }
}


async function downloadID(){

    const file =
        document.getElementById(
            "idFile"
        ).files[0];

    if(!file){

        alert(
            "Please upload an ID image."
        );

        return;
    }

    await processImage(
        file,
        "ID-Card",
        1013,
        638,
        "ID-Card-1013x638.jpg"
    );
}


async function downloadIDA4(){

    const image =
        getPreviewImage(
            "idFinal"
        );

    if(!image){

        alert(
            "Please upload an ID image."
        );

        return;
    }

    await downloadCanvasAsA4(
        image,
        "ID-Card-A4.pdf"
    );
}


/* =========================================================
   PASSPORT
========================================================= */

function passportTool(area,nameDate=false){

    area.innerHTML = `

    <div class="hero">

        <span class="pill">
            35 × 45 MM • 413 × 531 PX •
            300 DPI
        </span>

        <h1>
            ${
                nameDate
                ?
                "Name & Date Passport Photo"
                :
                "Indian Passport Photo"
            }
        </h1>

        <p>
            Standard 35 × 45 mm photo.
        </p>

    </div>


    <div class="card">

        <div class="drop-zone">

            <input
                id="passportFile"
                class="file-input"
                type="file"
                accept="image/*"
            >

            <span class="note">
                JPG / PNG
            </span>

        </div>


        <div class="dimension-panel">

            <div class="field">

                <label>
                    Preset
                </label>

                <select
                    id="passportPreset"
                    onchange="passportPresetChanged()"
                >

                    <option value="india">
                        India — 35×45 mm
                    </option>

                    <option value="2x2">
                        2×2 inch — 51×51 mm
                    </option>

                    <option value="custom">
                        Custom
                    </option>

                </select>

            </div>


            <div class="field">

                <label>
                    Width PX
                </label>

                <input
                    id="passportWidth"
                    value="413"
                    type="number"
                >

            </div>


            <div class="field">

                <label>
                    Height PX
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

                <select id="passportDPI">

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


        <div class="dimension-info">

            Selected:

            <strong id="passportDimensionText">
                35 × 45 mm • 413 × 531 px
            </strong>

        </div>

    </div>


    <div
        class="preview-layout"
        style="margin-top:18px"
    >

        <div class="card">

            <div class="preview-label">
                ORIGINAL
            </div>

            <div class="preview-box">

                <img
                    id="passportOriginal"
                    alt=""
                >

            </div>

        </div>


        <div class="card">

            <div class="preview-label">
                FINAL OUTPUT
            </div>

            <div class="preview-box">

                <img
                    id="passportFinal"
                    alt=""
                >

                <span class="note">
                    413 × 531 px @ 300 DPI
                </span>

            </div>

        </div>

    </div>


    <div class="card" style="margin-top:18px">

        <h3>
            A4 Print Preview
        </h3>

        <div class="print-preview-wrapper">

            <div
                id="passportA4Preview"
                class="a4-sheet"
            ></div>

        </div>


        <div class="download-row">

            <button
                class="btn btn-primary"
                onclick="downloadPassport()"
            >
                Download Passport
            </button>

            <button
                class="btn btn-success"
                onclick="downloadPassportA4()"
            >
                Download in A4
            </button>

        </div>

    </div>

    `;


    document
        .getElementById(
            "passportFile"
        )
        .addEventListener(
            "change",
            previewPassport
        );
}


function passportPresetChanged(){

    const preset =
        document.getElementById(
            "passportPreset"
        ).value;

    const width =
        document.getElementById(
            "passportWidth"
        );

    const height =
        document.getElementById(
            "passportHeight"
        );

    const text =
        document.getElementById(
            "passportDimensionText"
        );


    if(preset==="india"){

        width.value=413;
        height.value=531;

        text.innerText =
            "35 × 45 mm • 413 × 531 px";
    }


    if(preset==="2x2"){

        width.value=600;
        height.value=600;

        text.innerText =
            "51 × 51 mm • 600 × 600 px";
    }


    if(preset==="custom"){

        text.innerText =
            "Custom dimensions";
    }
}


function previewPassport(event){

    const file =
        event.target.files[0];

    if(!file)return;

    const url =
        URL.createObjectURL(file);

    document.getElementById(
        "passportOriginal"
    ).src=url;

    document.getElementById(
        "passportFinal"
    ).src=url;

    createPassportA4(url);
}


function createPassportA4(url){

    const sheet =
        document.getElementById(
            "passportA4Preview"
        );

    if(!sheet)return;

    sheet.innerHTML="";

    for(
        let i=0;
        i<24;
        i++
    ){

        sheet.innerHTML += `

            <img
                class="a4-passport"
                src="${url}"
                alt=""
            >

        `;
    }
}


async function downloadPassport(){

    const file =
        document.getElementById(
            "passportFile"
        ).files[0];

    if(!file){

        alert(
            "Please select photo."
        );

        return;
    }

    await processImage(
        file,
        "Passport-Photo",
        Number(
            document.getElementById(
                "passportWidth"
            ).value
        ),
        Number(
            document.getElementById(
                "passportHeight"
            ).value
        ),
        "Passport-Photo.jpg"
    );
}


async function downloadPassportA4(){

    const image =
        getPreviewImage(
            "passportFinal"
        );

    if(!image){

        alert(
            "Please select photo."
        );

        return;
    }

    await downloadCanvasAsA4(
        image,
        "Passport-Photos-A4.pdf"
    );
}


/* =========================================================
   4x6
========================================================= */

function fourSixTool(area){

    area.innerHTML = `

    <div class="hero">

        <span class="pill">
            4 × 6 INCH • 10.16 × 15.24 CM •
            1200 × 1800 PX @ 300 DPI
        </span>

        <h1>
            4×6 Photo Print
        </h1>

        <p>
            Standard 4×6 inch photo with live
            preview and A4 print-sheet generation.
        </p>

    </div>


    <div class="card">

        <div class="drop-zone">

            <input
                id="fourSixFile"
                class="file-input"
                type="file"
                accept="image/*"
            >

            <span class="note">
                JPG / PNG
            </span>

        </div>


        <div class="dimension-panel">

            <div class="field">

                <label>
                    Preset
                </label>

                <select>

                    <option selected>
                        4×6 inch
                    </option>

                </select>

            </div>


            <div class="field">

                <label>
                    Width
                </label>

                <input
                    value="1200"
                    disabled
                >

            </div>


            <div class="field">

                <label>
                    Height
                </label>

                <input
                    value="1800"
                    disabled
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


        <div class="dimension-info">

            Physical size:

            <strong>
                4 × 6 inch
            </strong>

            &nbsp; • &nbsp;

            10.16 × 15.24 cm

            &nbsp; • &nbsp;

            1200 × 1800 px @ 300 DPI

        </div>

    </div>


    <div
        class="preview-layout"
        style="margin-top:18px"
    >

        <div class="card">

            <div class="preview-label">
                ORIGINAL PREVIEW
            </div>

            <div class="preview-box">

                <img
                    id="fourSixOriginal"
                    alt=""
                >

            </div>

        </div>


        <div class="card">

            <div class="preview-label">
                FINAL 4×6 PREVIEW
            </div>

            <div class="preview-box">

                <img
                    id="fourSixFinal"
                    alt=""
                    style="
                        width:240px;
                        aspect-ratio:2/3;
                        object-fit:cover;
                    "
                >

                <span class="note">
                    1200 × 1800 px
                </span>

            </div>

        </div>

    </div>


    <div class="card" style="margin-top:18px">

        <h3>
            A4 Print Preview
        </h3>

        <p class="note">
            Photos are automatically arranged on
            an A4 sheet with print-safe spacing.
        </p>


        <div class="print-preview-wrapper">

            <div
                id="fourSixA4"
                class="a4-sheet photo-4x6"
            ></div>

        </div>


        <div class="download-row">

            <button
                class="btn btn-primary"
                onclick="download46()"
            >
                Download 4×6 JPG
            </button>

            <button
                class="btn btn-success"
                onclick="download46A4()"
            >
                Download in A4
            </button>

        </div>

    </div>

    `;


    document
        .getElementById(
            "fourSixFile"
        )
        .addEventListener(
            "change",
            preview46
        );
}


function preview46(event){

    const file =
        event.target.files[0];

    if(!file)return;

    const url =
        URL.createObjectURL(file);

    document.getElementById(
        "fourSixOriginal"
    ).src=url;

    document.getElementById(
        "fourSixFinal"
    ).src=url;

    create46A4(url);
}


function create46A4(url){

    const sheet =
        document.getElementById(
            "fourSixA4"
        );

    if(!sheet)return;

    sheet.innerHTML="";

    /*
       A4 portrait:
       210 × 297 mm

       4×6:
       101.6 × 152.4 mm

       Two 4×6 photos fit side-by-side
       with sensible margins.
    */

    for(
        let i=0;
        i<4;
        i++
    ){

        sheet.innerHTML += `

            <img
                class="a4-photo"
                src="${url}"
                alt=""
            >

        `;
    }
}


async function download46(){

    const file =
        document.getElementById(
            "fourSixFile"
        ).files[0];

    if(!file){

        alert(
            "Please select a photo."
        );

        return;
    }

    await processImage(
        file,
        "4x6-Photo",
        1200,
        1800,
        "4x6-1200x1800.jpg"
    );
}


async function download46A4(){

    const image =
        getPreviewImage(
            "fourSixFinal"
        );

    if(!image){

        alert(
            "Please select a photo."
        );

        return;
    }

    await downloadCanvasAsA4(
        image,
        "4x6-Photos-A4.pdf"
    );
}


/* =========================================================
   RESIZE
========================================================= */

function resizeTool(area){

    area.innerHTML = `

    <div class="hero">

        <span class="pill">
            GLOBAL DIMENSION PRESETS
        </span>

        <h1>
            Image Resizer
        </h1>

        <p>
            Choose a standard size or enter
            custom dimensions.
        </p>

    </div>


    <div class="card">

        <div class="drop-zone">

            <input
                id="resizeFile"
                class="file-input"
                type="file"
                accept="image/*"
            >

        </div>


        <div class="dimension-panel">

            <div class="field">

                <label>
                    Standard Size
                </label>

                <select
                    id="resizePreset"
                    onchange="resizePreset()"
                >

                    <option value="idCard">
                        ID Card — 1013×638
                    </option>

                    <option value="passport">
                        Passport — 413×531
                    </option>

                    <option value="photo4x6">
                        4×6 — 1200×1800
                    </option>

                    <option value="a4">
                        A4 — 2480×3508
                    </option>

                    <option value="a5">
                        A5 — 1748×2480
                    </option>

                    <option value="a3">
                        A3 — 3508×4961
                    </option>

                    <option value="square2x2">
                        2×2 — 600×600
                    </option>

                    <option value="custom">
                        Custom
                    </option>

                </select>

            </div>


            <div class="field">

                <label>
                    Width
                </label>

                <input
                    id="resizeWidth"
                    value="1013"
                    type="number"
                >

            </div>


            <div class="field">

                <label>
                    Height
                </label>

                <input
                    id="resizeHeight"
                    value="638"
                    type="number"
                >

            </div>


            <div class="field">

                <label>
                    DPI
                </label>

                <input
                    id="resizeDPI"
                    value="300"
                    type="number"
                >

            </div>

        </div>


        <div class="actions">

            <button
                class="btn btn-primary"
                onclick="downloadResize()"
            >
                Resize & Download
            </button>

        </div>

    </div>

    `;
}


function resizePreset(){

    const key =
        document.getElementById(
            "resizePreset"
        ).value;

    if(key==="custom")return;

    const d =
        DIMENSIONS[key];

    document.getElementById(
        "resizeWidth"
    ).value=d.width;

    document.getElementById(
        "resizeHeight"
    ).value=d.height;

    document.getElementById(
        "resizeDPI"
    ).value=d.dpi || 300;
}


async function downloadResize(){

    const file =
        document.getElementById(
            "resizeFile"
        ).files[0];

    if(!file){

        alert(
            "Please select an image."
        );

        return;
    }

    const width =
        Number(
            document.getElementById(
                "resizeWidth"
            ).value
        );

    const height =
        Number(
            document.getElementById(
                "resizeHeight"
            ).value
        );

    await processImage(
        file,
        "Image-Resize",
        width,
        height,
        "resized-image.jpg"
    );
}


/* =========================================================
   IMAGE TO PDF
========================================================= */

function imagePDFTool(area){

    area.innerHTML = `

    <div class="hero">

        <span class="pill">
            JPG • PNG → PDF
        </span>

        <h1>
            Image to PDF
        </h1>

    </div>


    <div class="card">

        <div class="drop-zone">

            <input
                id="pdfImages"
                class="file-input"
                type="file"
                accept="image/jpeg,image/png"
                multiple
            >

            <span class="note">
                Multiple images supported
            </span>

        </div>


        <div class="dimension-info">

            Default page:

            <strong>
                A4 • 210 × 297 mm •
                2480 × 3508 px @ 300 DPI
            </strong>

        </div>


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
                await response
                    .json();

            throw new Error(
                data.error
            );
        }

        const blob =
            await response.blob();

        downloadBlob(
            blob,
            "images-to-pdf.pdf"
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

        <div class="drop-zone">

            <input
                id="pdfFile"
                class="file-input"
                type="file"
                accept="application/pdf"
            >

        </div>


        <div class="dimension-panel">

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
            style="margin-top:18px"
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
            "Please choose a PDF."
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

            <div class="dimension-info">

                Pages:

                <strong>
                    ${data.pages}
                </strong>

            </div>

            ${
                data.dimensions
                    .map(
                        p => `

                        <div
                            class="history-row"
                        >

                            <span>
                                Page ${p.page}
                            </span>

                            <span>
                                ${p.width.toFixed(1)}
                                ×
                                ${p.height.toFixed(1)}
                                pt
                            </span>

                        </div>

                        `
                    )
                    .join("")
            }

        `;

    }catch(error){

        alert(error.message);
    }
}


/* =========================================================
   HISTORY
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
                SERVER SIDE • 30 DAYS
            </span>

            <h1>
                30-Day History
            </h1>

            <p>
                History is stored on the server,
                not browser storage.
            </p>

        </div>


        <div class="card">

            ${
                history.length
                ?
                history.map(
                    item => `

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

                    `
                ).join("")
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

            Unable to load history.

        </div>

        `;
    }
}


/* =========================================================
   IMAGE PROCESS
========================================================= */

async function processImage(
    file,
    tool,
    width,
    height,
    filename
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
            filename
        );

    }catch(error){

        alert(error.message);
    }
}


/* =========================================================
   GET PREVIEW IMAGE
========================================================= */

function getPreviewImage(id){

    const element =
        document.getElementById(id);

    if(!element)return null;

    if(element.tagName==="IMG"){

        return element.src || null;
    }

    const img =
        element.querySelector(
            "img"
        );

    return img
        ? img.src
        : null;
}


/* =========================================================
   CLIENT SIDE A4 PDF
========================================================= */

async function downloadCanvasAsA4(
    imageSrc,
    filename
){

    /*
       This generates a printable A4 canvas
       in the browser.

       For a true PDF file, backend should use
       a PDF library such as PDFKit/Puppeteer.
    */

    const img =
        new Image();

    img.onload =
        () => {

            const canvas =
                document.createElement(
                    "canvas"
                );

            /*
               A4 at 150 DPI for browser
               generation to keep memory reasonable.
            */

            canvas.width=1240;
            canvas.height=1754;

            const ctx =
                canvas.getContext(
                    "2d"
                );

            ctx.fillStyle="white";

            ctx.fillRect(
                0,
                0,
                canvas.width,
                canvas.height
            );


            /*
               Determine layout based on
               current tool.
            */

            const area =
                document.getElementById(
                    "customerToolArea"
                );

            const fourSix =
                !!area.querySelector(
                    "#fourSixA4"
                );

            const passport =
                !!area.querySelector(
                    "#passportA4Preview"
                );


            if(fourSix){

                drawRepeated(
                    ctx,
                    img,
                    2,
                    3,
                    110,
                    110,
                    560,
                    840
                );

            }else if(passport){

                drawRepeated(
                    ctx,
                    img,
                    4,
                    5,
                    130,
                    120,
                    245,
                    315
                );

            }else{

                drawRepeated(
                    ctx,
                    img,
                    2,
                    5,
                    80,
                    100,
                    1080,
                    400
                );
            }


            /*
               Download PNG representation.

               Production backend can convert
               this exact layout to PDF.
            */

            canvas.toBlob(
                blob => {

                    downloadBlob(
                        blob,
                        filename
                            .replace(
                                ".pdf",
                                ".png"
                            )
                    );

                },
                "image/png"
            );

        };

    img.src=imageSrc;
}


function drawRepeated(
    ctx,
    img,
    cols,
    rows,
    startX,
    startY,
    cellW,
    cellH
){

    let count=0;

    for(
        let row=0;
        row<rows;
        row++
    ){

        for(
            let col=0;
            col<cols;
            col++
        ){

            const x =
                startX +
                col *
                (cellW+20);

            const y =
                startY +
                row *
                (cellH+20);

            if(
                x+cellW >
                ctx.canvas.width ||
                y+cellH >
                ctx.canvas.height
            ){
                continue;
            }

            ctx.drawImage(
                img,
                x,
                y,
                cellW,
                cellH
            );

            count++;
        }
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

    a.href=url;

    a.download=filename;

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
   ADMIN DASHBOARD
========================================================= */

async function showAdmin(){

    document.getElementById(
        "app"
    ).innerHTML = `

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


    if(page==="dashboard"){

        const customers =
            await api(
                "/api/admin/customers"
            );

        const active =
            customers.filter(
                c => c.active
            ).length;

        area.innerHTML = `

        <h1>
            Admin Dashboard
        </h1>

        <p class="note">
            Customer account and payment management
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
                    ₹${customers.reduce(
                        (s,c)=>
                            s+
                            Number(
                                c.pending||0
                            ),
                        0
                    ).toLocaleString("en-IN")}
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


    if(page==="customers"){

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
            flex-wrap:wrap;
        ">

            <div>

                <h1>
                    Customers
                </h1>

                <p class="note">
                    Only Admin can create customer accounts.
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
                        customers.map(
                            c => `

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
                                            ?
                                            "badge-green"
                                            :
                                            "badge-yellow"
                                        }"
                                    >

                                        ${
                                            c.active
                                            ?
                                            "Active"
                                            :
                                            "Inactive"
                                        }

                                    </span>

                                </td>

                                <td>
                                    ${c.daysLeft}
                                    Days
                                </td>

                                <td>

                                    <button
                                        class="btn btn-small"
                                        onclick="
                                            toggleCustomer(
                                                ${c.id},
                                                ${!c.active}
                                            )
                                        "
                                    >

                                        ${
                                            c.active
                                            ?
                                            "Disable"
                                            :
                                            "Enable"
                                        }

                                    </button>

                                </td>

                            </tr>

                            `
                        ).join("")
                    }

                    </tbody>

                </table>

            </div>

        </div>

        `;

        return;
    }


    if(page==="payments"){

        const payments =
            await api(
                "/api/admin/payments"
            );

        area.innerHTML = `

        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            gap:15px;
            flex-wrap:wrap;
        ">

            <div>

                <h1>
                    Payments
                </h1>

                <p class="note">
                    Customer payment records
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
                        payments.map(
                            p => `

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

                            `
                        ).join("")
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

    const days =
        prompt(
            "Validity Days:",
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
                            Number(days)

                    })
                }
            );

        alert(
            "Customer created successfully.\n\n"+
            "Username: "+
            result.username+
            "\nExpiry: "+
            new Date(
                result.expiresAt
            ).toLocaleDateString()
        );

        adminPage(
            "customers"
        );

    }catch(error){

        alert(
            error.message
        );
    }
}


/* =========================================================
   CUSTOMER STATUS
========================================================= */

async function toggleCustomer(
    id,
    active
){

    try{

        await api(
            "/api/admin/customers/"+id,
            {
                method:"PATCH",

                body:JSON.stringify({
                    active
                })
            }
        );

        adminPage(
            "customers"
        );

    }catch(error){

        alert(
            error.message
        );
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

    const id =
        prompt(
            "Customer ID:\n\n"+
            list
        );

    if(!id)return;

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
                        Number(id),

                    amount:
                        Number(amount),

                    status:
                        "Paid"

                })
            }
        );

        alert(
            "Payment recorded."
        );

        adminPage(
            "payments"
        );

    }catch(error){

        alert(
            error.message
        );
    }
}


/* =========================================================
   START
========================================================= */

start();

</script>

</body>
</html>
