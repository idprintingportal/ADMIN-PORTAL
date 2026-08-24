<!-- CUSTOMER DASHBOARD -->

<div class="customer-portal">

    <header class="portal-header">

        <div class="portal-title">
            <h1>ID CARD PRINT & CONVERTER PORTAL</h1>
        </div>

        <div class="top-actions">
            <button class="top-btn admin-btn"
                    onclick="openAdminLogin()">
                🔐 Admin Login
            </button>
        </div>

    </header>


    <!-- TOOL BUTTONS -->

    <nav class="tools">

        <button class="tool-btn active"
                onclick="openTool('idcard')">
            🪪 ID Card (5 Slots)
        </button>

        <button class="tool-btn"
                onclick="openTool('passport')">
            👤 Passport Photos
        </button>

        <button class="tool-btn"
                onclick="openTool('namePassport')">
            📄 Name & Date Passport
        </button>

        <button class="tool-btn"
                onclick="openTool('photo46')">
            🖼️ 4×6 Photo Print
        </button>

        <button class="tool-btn"
                onclick="openTool('arranger')">
            📑 PDF Arranger
        </button>

        <button class="tool-btn"
                onclick="openTool('imageToPdf')">
            📄 PDF, JPG, PNG to PDF
        </button>

        <button class="tool-btn"
                onclick="openTool('resizer')">
            📐 Image Resizer
        </button>

        <button class="tool-btn"
                onclick="openTool('pdfJpg')">
            🖼️ PDF to JPG (Manual DPI)
        </button>

        <button class="tool-btn"
                onclick="openTool('compressor')">
            🗜️ PDF Compressor
        </button>

        <button class="tool-btn"
                onclick="openTool('history')">
            📁 30-Day History
        </button>

    </nav>


    <!-- CUSTOMER ACCOUNT BAR -->

    <section class="account-bar">

        <div class="validity">
            ⏳ Account Validity:
            <strong>365 Days Left</strong>
            <span>(of 365 Days)</span>
        </div>

        <button class="logout-btn"
                onclick="customerLogout()">
            🔒 Logout
        </button>

    </section>


    <!-- CURRENT TOOL -->

    <main id="toolArea">

        <div class="tool-info">

            <div class="info-badge">
                AUTO-DIMENSION CROP • 2.5MM GAP •
                BROAD BLACK BORDER • 5 CARDS
            </div>

            <h2>
                Card Generator System
            </h2>

            <p>
                इमेज सिलेक्ट करते ही वह ऑटोमेटिकली सही
                ID साइज में फिट हो जाएगी। जरूरत पड़ने पर
                मैनुअल क्रॉप भी कर सकते हैं।
            </p>

            <div class="slot-count">
                Cards on Page: <strong>0 / 5</strong>
                <span>(Next Slot: #1)</span>
            </div>

        </div>


        <!-- FRONT / BACK -->

        <div class="card-upload-grid">

            <div class="upload-box">

                <div class="upload-title">
                    📁 Front Side
                </div>

                <p>
                    इमेज चुनें (Auto-Crop)
                </p>

                <input
                    type="file"
                    accept="image/*"
                    id="frontImage"
                    onchange="previewImage(this,'frontPreview')"
                >

            </div>


            <div class="upload-box">

                <div class="upload-title">
                    📁 Back Side
                </div>

                <p>
                    इमेज चुनें (Auto-Crop)
                </p>

                <input
                    type="file"
                    accept="image/*"
                    id="backImage"
                    onchange="previewImage(this,'backPreview')"
                >

            </div>

        </div>


        <div class="preview-grid">

            <div class="preview-card">

                <h3>Front Card Preview</h3>

                <img id="frontPreview"
                     alt="Front Preview">

            </div>


            <div class="preview-card">

                <h3>Back Card Preview</h3>

                <img id="backPreview"
                     alt="Back Preview">

            </div>

        </div>

    </main>

</div>


<style>

.customer-portal{
    min-height:100vh;
    background:
        radial-gradient(
            circle at 50% 0%,
            rgba(150,80,255,.12),
            transparent 35%
        ),
        #0a0710;
    color:#fff;
    padding:22px 35px;
}

.portal-header{
    display:flex;
    align-items:center;
    justify-content:space-between;
    border-bottom:1px solid #4b3a55;
    padding-bottom:16px;
}

.portal-title h1{
    text-align:center;
    font-size:25px;
    letter-spacing:1px;
    background:linear-gradient(
        90deg,
        #9f8cff,
        #ff5dbd
    );
    -webkit-background-clip:text;
    color:transparent;
}

.top-btn,
.tool-btn,
.logout-btn{
    border:1px solid #40344d;
    color:#fff;
    background:#191321;
    border-radius:11px;
    cursor:pointer;
    transition:.2s;
}

.admin-btn{
    padding:10px 15px;
}

.admin-btn:hover{
    border-color:#8e73ff;
    background:#211934;
}

.tools{
    display:flex;
    flex-wrap:wrap;
    justify-content:center;
    gap:9px;
    padding:18px 0;
}

.tool-btn{
    padding:11px 15px;
    font-size:13px;
}

.tool-btn:hover{
    border-color:#806cff;
    transform:translateY(-1px);
}

.tool-btn.active{
    background:linear-gradient(
        135deg,
        #617fff,
        #826eff
    );
    border-color:#8fa1ff;
}

.account-bar{
    min-height:80px;
    border:1px solid #403a49;
    border-radius:20px;
    background:rgba(25,22,32,.85);
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding:18px 25px;
}

.validity{
    border:1px solid #5b975e;
    background:#17251a;
    color:#8ee18d;
    padding:10px 16px;
    border-radius:25px;
    font-size:13px;
}

.validity strong{
    color:#ffc83d;
}

.validity span{
    color:#b6c5b3;
}

.logout-btn{
    padding:10px 18px;
    background:#652f35;
    border-color:#9c4c54;
}

.tool-info{
    text-align:center;
    padding:35px 15px 20px;
}

.info-badge{
    display:inline-block;
    padding:9px 20px;
    border:1px solid #6684a9;
    border-radius:25px;
    color:#a8d9ff;
    background:#172435;
    font-size:12px;
}

.tool-info h2{
    font-size:35px;
    margin:35px 0 12px;
    background:linear-gradient(
        90deg,
        #b58cff,
        #ff63d2
    );
    -webkit-background-clip:text;
    color:transparent;
}

.tool-info p{
    color:#c8c2cc;
    font-size:14px;
}

.slot-count{
    display:inline-block;
    margin-top:15px;
    padding:9px 18px;
    border-radius:20px;
    background:#493226;
    border:1px solid #a87b51;
    color:#ffc85c;
}

.card-upload-grid{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:20px;
    max-width:1200px;
    margin:auto;
}

.upload-box{
    min-height:145px;
    border:2px dashed #69718b;
    border-radius:17px;
    background:#11101a;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    gap:9px;
}

.upload-title{
    font-size:17px;
    font-weight:bold;
}

.upload-box p{
    color:#aaa4b0;
    font-size:13px;
}

.upload-box input{
    max-width:250px;
}

.preview-grid{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:25px;
    max-width:750px;
    margin:20px auto;
}

.preview-card{
    background:#15131d;
    border:1px solid #393345;
    border-radius:15px;
    padding:15px;
    text-align:center;
}

.preview-card h3{
    font-size:14px;
    margin-bottom:10px;
}

.preview-card img{
    width:100%;
    max-height:350px;
    object-fit:contain;
    border-radius:8px;
}

@media(max-width:700px){

    .customer-portal{
        padding:15px;
    }

    .portal-title h1{
        font-size:17px;
    }

    .card-upload-grid,
    .preview-grid{
        grid-template-columns:1fr;
    }

    .account-bar{
        flex-direction:column;
        gap:15px;
    }

}

</style>


<script>

function openTool(tool){

    document.querySelectorAll(".tool-btn")
        .forEach(btn =>
            btn.classList.remove("active")
        );

    event.currentTarget.classList.add("active");

    /*
       यहाँ बाद में actual tools load होंगे:
       idcard
       passport
       namePassport
       photo46
       arranger
       imageToPdf
       resizer
       pdfJpg
       compressor
       history
    */

    console.log("Opening:",tool);
}


function previewImage(input,target){

    if(!input.files.length){
        return;
    }

    const file=input.files[0];

    const url=URL.createObjectURL(file);

    document.getElementById(target).src=url;

}


function customerLogout(){

    /*
       Production में backend session/token
       भी destroy किया जाएगा.
    */

    window.location.href="login.html";

}


function openAdminLogin(){

    window.location.href="admin-login.html";

}

</script>
