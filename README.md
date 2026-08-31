<!DOCTYPE html>
<html lang="hi">
<head>
<meta name="referrer" content="no-referrer">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ID CARD PRINT & CONVERTER PORTAL</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  
  <!-- PDF.js Standalone -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.min.js"></script>
  
  <!-- PDF-LIB for Pure Vector Merging & Page Manipulation -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf-lib/1.17.1/pdf-lib.min.js"></script>

  <!-- jsPDF Library -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>

  <!-- JSZip for Multi-page PDF to JPG Batch Download -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>

  <!-- Cropper.js -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/cropperjs/1.5.13/cropper.min.css"/>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/cropperjs/1.5.13/cropper.min.js"></script>

  <style>
    :root {
      --bg-gradient: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
      --card-bg: rgba(30, 41, 59, 0.88);
      --accent-blue: #38bdf8;
      --accent-purple: #818cf8;
      --btn-add: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
      --btn-download: linear-gradient(135deg, #10b981 0%, #059669 100%);
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --border-color: rgba(255, 255, 255, 0.1);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Poppins', sans-serif; }
    
    body { 
      background: var(--bg-gradient); 
      min-height: 100vh;
      padding: 15px 10px; 
      display: flex; 
      flex-direction: column; 
      align-items: center; 
      justify-content: center;
      color: var(--text-main);
    }

    .portal-main-heading {
      font-size: 24px;
      font-weight: 800;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      background: linear-gradient(135deg, #38bdf8 0%, #a855f7 50%, #f43f5e 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 10px;
      text-align: center;
    }

    /* Running Ticker Notification Bar */
    .ticker-container {
      width: 100%;
      max-width: 580px;
      overflow: hidden;
      background: rgba(56, 189, 248, 0.1);
      border: 1px solid rgba(56, 189, 248, 0.3);
      border-radius: 8px;
      padding: 8px 0;
      margin-bottom: 12px;
      white-space: nowrap;
    }

    .ticker-text {
      display: inline-block;
      padding-left: 100%;
      animation: tickerAnimation 18s linear infinite;
      color: #38bdf8;
      font-weight: 600;
      font-size: 13px;
    }

    @keyframes tickerAnimation {
      0% { transform: translate3d(0, 0, 0); }
      100% { transform: translate3d(-100%, 0, 0); }
    }

    /* Advertisement Image Slider / Grid */
    .ad-slider-box {
      display: flex;
      gap: 8px;
      justify-content: center;
      margin-bottom: 12px;
      max-width: 580px;
      width: 100%;
    }

    .ad-slide-img {
      width: calc(33.333% - 6px);
      height: 95px;
      object-fit: cover;
      border-radius: 8px;
      border: 1px solid var(--border-color);
      box-shadow: 0 4px 10px rgba(0,0,0,0.4);
      background: #1e293b;
      transition: transform 0.3s;
    }
    .ad-slide-img:hover { transform: scale(1.04); }

    /* Services Info Box */
    .services-info-card {
      background: rgba(15, 23, 42, 0.75);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 10px 14px;
      max-width: 580px;
      width: 100%;
      margin-bottom: 15px;
      text-align: left;
    }

    .services-info-card h4 {
      font-size: 12px;
      color: var(--accent-blue);
      margin-bottom: 4px;
      font-weight: 700;
    }

    .services-info-card ul {
      font-size: 11px;
      color: var(--text-muted);
      padding-left: 14px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 3px;
    }

    .top-reg-nav {
      display: flex;
      gap: 12px;
      margin-bottom: 15px;
      flex-wrap: wrap;
      justify-content: center;
    }

    .top-reg-btn {
      background: linear-gradient(135deg, #10b981 0%, #059669 100%);
      border: none;
      color: #fff;
      padding: 10px 22px;
      font-size: 13px;
      font-weight: 600;
      border-radius: 20px;
      cursor: pointer;
      transition: 0.3s;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
    }
    .top-reg-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(16, 185, 129, 0.6); }

    .auth-box {
      background: var(--card-bg);
      backdrop-filter: blur(20px);
      border: 1px solid var(--border-color);
      padding: 20px 25px;
      border-radius: 20px;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6);
      width: 100%;
      max-width: 580px;
      text-align: center;
    }

    .badge {
      display: inline-block;
      padding: 3px 12px;
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 1px;
      text-transform: uppercase;
      background: rgba(56, 189, 248, 0.15);
      color: var(--accent-blue);
      border: 1px solid rgba(56, 189, 248, 0.3);
      border-radius: 20px;
      margin-bottom: 8px;
    }

    .slot-counter-badge {
      background: rgba(245, 158, 11, 0.15);
      color: #fbbf24;
      border: 1px solid rgba(245, 158, 11, 0.3);
      padding: 4px 16px;
      font-size: 12px;
      font-weight: 600;
      border-radius: 20px;
      display: inline-block;
      margin-bottom: 15px;
    }

    .login-input {
      width: 100%;
      padding: 11px 15px;
      margin-bottom: 12px;
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid rgba(56, 189, 248, 0.3);
      border-radius: 10px;
      color: #fff;
      font-size: 13px;
      outline: none;
    }

    .login-btn {
      width: 100%;
      padding: 12px;
      background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%);
      color: #fff;
      font-weight: 600;
      border: none;
      border-radius: 10px;
      cursor: pointer;
      font-size: 14px;
      transition: 0.3s;
    }

    .auth-link {
      display: inline-block;
      margin-top: 10px;
      font-size: 12px;
      color: var(--accent-blue);
      cursor: pointer;
      text-decoration: underline;
    }

    .error-msg {
      color: #ef4444;
      font-size: 12px;
      margin-top: 10px;
      display: none;
    }

    .tab-nav {
      display: flex;
      justify-content: center;
      gap: 8px;
      margin-bottom: 15px;
      flex-wrap: wrap;
    }

    .tab-btn {
      padding: 9px 13px;
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      border-radius: 12px;
      cursor: pointer;
      font-weight: 600;
      font-size: 12px;
      transition: 0.3s;
    }

    .tab-btn.active {
      background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%);
      color: #fff;
      border-color: transparent;
      box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
    }

    #mainApp {
      display: none;
      width: 100%;
      max-width: 1220px;
    }

    .container { 
      background: var(--card-bg); 
      backdrop-filter: blur(16px);
      border: 1px solid var(--border-color);
      padding: 25px 20px; 
      border-radius: 20px; 
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4); 
      width: 100%; 
      text-align: center; 
      position: relative; 
    }

    .logout-btn {
      background: rgba(239, 68, 68, 0.2);
      border: 1px solid rgba(239, 68, 68, 0.4);
      color: #fca5a5;
      padding: 6px 14px;
      font-size: 12px;
      border-radius: 8px;
      cursor: pointer;
      transition: 0.2s;
    }
    .logout-btn:hover {
      background: rgba(239, 68, 68, 0.4);
    }

    h1 { 
      background: linear-gradient(to right, #38bdf8, #a855f7, #ec4899);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      font-size: 22px; 
      font-weight: 700;
      margin-bottom: 6px; 
    }

    .tab-content { display: none; }
    .tab-content.active { display: block; }

    .upload-section { 
      display: flex; 
      gap: 15px; 
      justify-content: center; 
      margin: 15px 0; 
      flex-wrap: wrap; 
    }

    .upload-box { 
      border: 2px dashed rgba(56, 189, 248, 0.4); 
      padding: 16px 14px; 
      border-radius: 14px; 
      cursor: pointer; 
      background: rgba(15, 23, 42, 0.6); 
      flex: 1; 
      min-width: 220px; 
      transition: 0.3s; 
    }

    .upload-box:hover { 
      border-color: var(--accent-blue);
      background: rgba(56, 189, 248, 0.08);
    }

    input[type="file"] { display: none; }

    .preview-container { 
      display: flex; 
      justify-content: center; 
      gap: 20px; 
      margin: 15px 0; 
      flex-wrap: wrap; 
    }

    .preview-box { 
      border: 1px solid var(--border-color); 
      padding: 10px; 
      background: rgba(15, 23, 42, 0.8); 
      border-radius: 12px; 
    }

    .preview-box h4 { 
      font-size: 12px; 
      color: var(--text-muted); 
      margin-bottom: 6px; 
    }
    
    canvas { 
      max-width: 100% !important; 
      height: auto !important; 
      display: block; 
      margin: 0 auto; 
      border-radius: 4px;
      background: #fff; 
      object-fit: contain;
    }

    .btn-group { 
      display: flex; 
      gap: 10px; 
      justify-content: center; 
      margin-top: 15px; 
      flex-wrap: wrap; 
    }

    .action-btn { 
      padding: 10px 22px; 
      font-size: 13px; 
      font-weight: 600; 
      border: none; 
      border-radius: 10px; 
      cursor: pointer; 
      transition: all 0.3s ease; 
      color: #fff;
    }

    .action-btn:hover:not(:disabled) {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(0,0,0,0.4);
    }

    .btn-add { background: var(--btn-add); }
    .btn-download { background: var(--btn-download); }
    .btn-reset { background: rgba(239, 68, 68, 0.2); border: 1px solid rgba(239, 68, 68, 0.4); color: #fca5a5; }

    .btn-manual-crop {
      background: rgba(56, 189, 248, 0.15);
      border: 1px solid var(--accent-blue);
      color: var(--accent-blue);
      padding: 4px 10px;
      font-size: 11px;
      border-radius: 6px;
      margin-top: 8px;
      cursor: pointer;
      font-weight: 600;
      transition: 0.2s;
    }
    .btn-manual-crop:hover {
      background: var(--accent-blue);
      color: #0f172a;
    }

    .action-btn:disabled { 
      background: #334155; 
      color: #64748b; 
      cursor: not-allowed; 
    }

    .control-panel {
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      padding: 14px 18px;
      max-width: 600px;
      margin: 15px auto;
      text-align: center;
    }

    .qty-select-group {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      margin-top: 8px;
      flex-wrap: wrap;
    }

    .qty-input {
      width: 80px;
      padding: 6px 10px;
      border-radius: 8px;
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid var(--accent-blue);
      color: #fff;
      font-size: 14px;
      font-weight: 700;
      text-align: center;
      outline: none;
    }

    .text-field-input {
      width: 100%;
      max-width: 260px;
      padding: 8px 12px;
      border-radius: 8px;
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid var(--accent-blue);
      color: #fff;
      font-size: 13px;
      outline: none;
      margin-bottom: 4px;
    }

    .quick-qty-btn {
      padding: 5px 12px;
      background: #334155;
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: #fff;
      border-radius: 6px;
      font-size: 11px;
      cursor: pointer;
      font-weight: 600;
    }

    .slider-range {
      -webkit-appearance: none;
      width: 100%;
      height: 6px;
      border-radius: 5px;
      background: #334155;
      outline: none;
      margin: 6px 0 8px 0;
    }

    .slider-range::-webkit-slider-thumb {
      -webkit-appearance: none;
      appearance: none;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: var(--accent-blue);
      cursor: pointer;
      box-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
    }

    .size-badge-box {
      display: flex;
      justify-content: space-around;
      background: rgba(15, 23, 42, 0.8);
      padding: 12px;
      border-radius: 10px;
      margin-top: 10px;
      border: 1px solid var(--border-color);
    }

    .file-gallery-list {
      display: flex;
      flex-wrap: wrap;
      gap: 14px;
      justify-content: center;
      margin: 15px 0;
      max-height: 420px;
      overflow-y: auto;
      padding: 14px;
      background: rgba(15, 23, 42, 0.6);
      border-radius: 12px;
      border: 1px solid var(--border-color);
    }

    .draggable-card {
      position: relative;
      width: 125px;
      background: #0f172a;
      border: 2px solid rgba(56, 189, 248, 0.35);
      border-radius: 10px;
      padding: 6px 4px 8px 4px;
      display: flex;
      flex-direction: column;
      align-items: center;
      box-shadow: 0 6px 14px rgba(0,0,0,0.5);
      cursor: grab;
      user-select: none;
      transition: transform 0.2s ease, border-color 0.2s ease, opacity 0.2s ease;
    }

    .draggable-card:active { cursor: grabbing; }
    .draggable-card.dragging { opacity: 0.4; transform: scale(0.92); border-color: #f59e0b; }
    .draggable-card.drag-over { border: 2px dashed #38bdf8; transform: scale(1.05); background: rgba(56, 189, 248, 0.12); }

    .draggable-card canvas, .draggable-card img {
      width: 100%;
      height: 135px;
      object-fit: contain;
      background: #ffffff;
      border-radius: 5px;
      pointer-events: none;
    }

    .draggable-card .file-label {
      font-size: 11px;
      color: #94a3b8;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      width: 100%;
      margin: 6px 0 2px 0;
      font-weight: 600;
      text-align: center;
      pointer-events: none;
    }

    .card-tools-bar {
      display: flex;
      gap: 6px;
      justify-content: center;
      width: 100%;
      margin-top: 4px;
    }

    .mini-tool-btn {
      background: #334155;
      color: #f8fafc;
      border: 1px solid rgba(255,255,255,0.15);
      border-radius: 4px;
      padding: 4px 8px;
      font-size: 11px;
      cursor: pointer;
      transition: 0.2s;
    }
    .mini-tool-btn:hover { background: #0284c7; }
    .mini-tool-btn.btn-del:hover { background: #ef4444; }

    .item-delete-btn {
      position: absolute;
      top: -6px;
      right: -6px;
      background: #ef4444;
      color: #ffffff;
      border: 2px solid #1e293b;
      border-radius: 50%;
      width: 22px;
      height: 22px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 11px;
      font-weight: bold;
      cursor: pointer;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.5);
      z-index: 10;
      transition: 0.2s;
    }
    .item-delete-btn:hover { background: #dc2626; transform: scale(1.15); }

    .history-table-container {
      margin-top: 15px;
      overflow-x: auto;
      background: rgba(15, 23, 42, 0.7);
      border-radius: 12px;
      border: 1px solid var(--border-color);
    }

    .history-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
      text-align: left;
    }

    .history-table th, .history-table td {
      padding: 10px 14px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }

    .history-table th {
      background: rgba(30, 41, 59, 0.9);
      color: var(--accent-blue);
      font-weight: 600;
    }

    .history-table tr:hover { background: rgba(56, 189, 248, 0.05); }

    .history-download-btn {
      background: #0284c7;
      color: #fff;
      border: none;
      padding: 5px 12px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 11px;
      font-weight: 600;
    }

    .history-delete-btn {
      background: rgba(239, 68, 68, 0.2);
      color: #fca5a5;
      border: 1px solid rgba(239, 68, 68, 0.4);
      padding: 5px 12px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 11px;
      font-weight: 600;
      transition: 0.2s;
    }
    .history-delete-btn:hover { background: rgba(239, 68, 68, 0.4); }

    .history-msg-btn {
      background: rgba(245, 158, 11, 0.2);
      color: #fbbf24;
      border: 1px solid rgba(245, 158, 11, 0.4);
      padding: 5px 12px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 11px;
      font-weight: 600;
      transition: 0.2s;
      margin-left: 5px;
    }
    .history-msg-btn:hover { background: rgba(245, 158, 11, 0.4); }

    .history-view-ss-btn {
      background: rgba(56, 189, 248, 0.25);
      color: #38bdf8;
      border: 1px solid rgba(56, 189, 248, 0.5);
      padding: 5px 10px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 11px;
      font-weight: 600;
      transition: 0.2s;
      margin-left: 5px;
    }
    .history-view-ss-btn:hover { background: rgba(56, 189, 248, 0.45); }

    /* Separate Stop and Start Buttons */
    .btn-status-stop {
      background: rgba(239, 68, 68, 0.25);
      color: #fca5a5;
      border: 1px solid rgba(239, 68, 68, 0.5);
      padding: 5px 10px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 11px;
      font-weight: 600;
      transition: 0.2s;
      margin-left: 5px;
    }
    .btn-status-stop:hover { background: rgba(239, 68, 68, 0.45); }

    .btn-status-start {
      background: rgba(16, 185, 129, 0.25);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.5);
      padding: 5px 10px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 11px;
      font-weight: 600;
      transition: 0.2s;
      margin-left: 5px;
    }
    .btn-status-start:hover { background: rgba(16, 185, 129, 0.45); }

    #cropModal, #adminMsgModal, #viewScreenshotModal {
      display: none;
      position: fixed;
      top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(0, 0, 0, 0.85);
      z-index: 10000;
      align-items: center;
      justify-content: center;
      flex-direction: column;
      padding: 20px;
    }

    .crop-wrapper {
      max-width: 90vw;
      max-height: 70vh;
      background: #000;
      border-radius: 8px;
      overflow: hidden;
      margin-bottom: 15px;
    }

    .crop-wrapper img {
      max-width: 100%;
      max-height: 70vh;
      display: block;
    }

    /* Registration Modal Popup Styles */
    #regModalPopup {
      display: none;
      position: fixed;
      top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(0, 0, 0, 0.85);
      z-index: 1000000;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }

    .reg-popup-content {
      background: #1e293b;
      border: 1px solid rgba(56, 189, 248, 0.4);
      border-radius: 16px;
      padding: 25px;
      width: 100%;
      max-width: 420px;
      text-align: center;
      box-shadow: 0 25px 60px rgba(0,0,0,0.8);
    }

    #paymentQrImage { display: none !important; }

    .payment-link-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 100%;
      max-width: 280px;
      padding: 11px 16px;
      background: linear-gradient(135deg, #10b981 0%, #059669 100%);
      color: #fff;
      border-radius: 9px;
      font-size: 13px;
      font-weight: 700;
      text-decoration: none;
      box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
    }
      /* Opaque defaults keep host-site table styles from making rows white. */
    #tab-admin .history-table-container,
    #tab-admin .history-table {
      background: #0f172a !important;
      color: #f1f5f9 !important;
      color-scheme: dark;
    }
    #tab-admin .history-table thead th {
      background: #263449 !important;
      color: #7dd3fc !important;
      border-color: #475569 !important;
    }
    #tab-admin .history-table tbody tr,
    #tab-admin .history-table tbody tr > td {
      background: #172033 !important;
      color: #f1f5f9 !important;
      border-color: #334155 !important;
      box-shadow: none !important;
      opacity: 1;
    }
    #tab-admin .history-table tbody tr:nth-child(even),
    #tab-admin .history-table tbody tr:nth-child(even) > td {
      background: #1e293b !important;
    }
    #tab-admin .history-table tbody tr:hover,
    #tab-admin .history-table tbody tr:hover > td {
      background: #29394f !important;
    }
    #tab-admin .history-table .history-msg-btn {
      background: #3a2b16 !important;
      color: #fde68a !important;
      border: 1px solid #b7832f !important;
      opacity: 1;
    }
    #tab-admin .history-table .history-msg-btn:hover,
    #tab-admin .history-table .history-msg-btn:focus-visible {
      background: #57401d !important;
      color: #fff3c4 !important;
    }
    #tab-admin .history-table .history-msg-btn:focus-visible {
      outline: 2px solid #7dd3fc;
      outline-offset: 2px;
    }
    #tab-admin .history-table .history-msg-btn:disabled {
      background: #334155 !important;
      color: #cbd5e1 !important;
      cursor: wait;
    }

</style>
<style>
#tab-pdf-editor .pe-shell{background:#111b2d;border:1px solid #34435c;border-radius:16px;overflow:hidden;text-align:left;color:#e8eef8}
#tab-pdf-editor .pe-heading{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:24px;background:#172338}
#tab-pdf-editor h1{font-size:26px;margin:2px 0 5px;text-align:left;color:#f8fafc;background:none;-webkit-text-fill-color:initial}
#tab-pdf-editor .pe-eyebrow{font-size:10px;color:#67d9fa;letter-spacing:2px;font-weight:700}
#tab-pdf-editor p{font-size:12px;line-height:1.8;color:#bdc9dc}
#tab-pdf-editor button{background:#24334b;color:#f1f5f9;border:1px solid #4b5e7a;border-radius:7px;padding:9px 12px;font-size:12px;cursor:pointer;font-weight:500;white-space:nowrap}
#tab-pdf-editor button:hover{background:#344962}
#tab-pdf-editor button:focus-visible,#tab-pdf-editor input:focus-visible,#tab-pdf-editor textarea:focus-visible,#tab-pdf-editor select:focus-visible{outline:2px solid #67e8f9;outline-offset:2px}
#tab-pdf-editor button:disabled{opacity:.4;cursor:not-allowed}
#tab-pdf-editor .pe-primary{background:#147d8a;border-color:#43c4d4;color:white;font-weight:600}
#tab-pdf-editor .pe-danger{color:#fda4af;border-color:#88434e}
#tab-pdf-editor .pe-filebar{display:flex;align-items:center;gap:12px;flex-wrap:wrap;padding:15px 20px;border-bottom:1px solid #334155}
#tab-pdf-editor #pe-filename{flex:1;font-size:12px;overflow-wrap:anywhere;min-width:120px;color:#c8d5e8}
#tab-pdf-editor .pe-notice{padding:10px 20px;background:#332b1b;color:#f4d6a0;font-size:11px}
#tab-pdf-editor fieldset{border:0;margin:0;padding:0;min-width:0}
#tab-pdf-editor .pe-toolbar,#tab-pdf-editor .pe-options{display:flex;align-items:center;gap:7px;flex-wrap:wrap;padding:12px 16px;border-bottom:1px solid #34435c}
#tab-pdf-editor button[aria-pressed=true]{background:#124951;color:#a5f3fc;border-color:#43c4d4}
#tab-pdf-editor label{display:inline-flex;align-items:center;gap:7px;font-size:11px;color:#cbd5e1}
#tab-pdf-editor input,#tab-pdf-editor select,#tab-pdf-editor textarea{background:#111b2d;border:1px solid #52637f;color:#f1f5f9;border-radius:5px;padding:6px;font-size:12px}
#tab-pdf-editor input[type=number]{width:64px}
#tab-pdf-editor input[type=color]{width:38px;height:31px;padding:3px}
#tab-pdf-editor .pe-workspace{display:grid;grid-template-columns:210px minmax(0,1fr);min-height:560px}
#tab-pdf-editor .pe-sidebar{padding:17px;border-right:1px solid #34435c;display:flex;flex-direction:column;gap:11px}
#tab-pdf-editor h3{font-size:13px;color:#f1f5f9}
#tab-pdf-editor textarea{width:100%;resize:vertical}
#tab-pdf-editor .pe-row{display:flex;gap:5px}
#tab-pdf-editor .pe-row button{padding:7px;font-size:10px;flex:1}
#tab-pdf-editor .pe-muted{font-size:11px;color:#a9bcd4}
#tab-pdf-editor hr{border:0;border-top:1px solid #34435c;margin:6px 0}
#tab-pdf-editor .pe-pagination{padding:10px;display:flex;align-items:center;justify-content:center;gap:10px;flex-wrap:wrap;background:#1b293e;font-size:12px}
#tab-pdf-editor #pe-scroll{background:#0a1220;overflow:auto;height:660px;padding:22px;position:relative}
#tab-pdf-editor #pe-page-wrap{position:relative;margin:0 auto;box-shadow:0 8px 30px #0006;flex-shrink:0}
#tab-pdf-editor #pe-page-wrap canvas{display:block;max-width:none!important;max-height:none!important;border:0!important;border-radius:0!important;box-shadow:none!important;margin:0!important}
#tab-pdf-editor #pe-base{background:white}
#tab-pdf-editor #pe-overlay{position:absolute;left:0;top:0;touch-action:none;cursor:crosshair}
#tab-pdf-editor #pe-empty{text-align:center;padding:100px 10px;color:#dce8f8}
#tab-pdf-editor #pe-empty span{font-size:62px;color:#42bdd0}
#tab-pdf-editor #pe-empty h2{font-size:20px;margin:15px 0}
#tab-pdf-editor #pe-status{padding:13px 20px;border-top:1px solid #34435c;font-size:12px;color:#9de0ed}
@media(max-width:720px){#tab-pdf-editor .pe-heading{padding:16px;align-items:flex-start;flex-direction:column}#tab-pdf-editor .pe-workspace{grid-template-columns:minmax(0,1fr)}#tab-pdf-editor .pe-sidebar{border-right:0;border-bottom:1px solid #34435c}#tab-pdf-editor .pe-sidebar p,#tab-pdf-editor .pe-sidebar hr,#tab-pdf-editor .pe-sidebar h3{display:none}#tab-pdf-editor #pe-scroll{height:520px;padding:12px}#tab-pdf-editor .pe-toolbar{gap:5px}#tab-pdf-editor .pe-toolbar button{padding:8px;font-size:11px}}

</style>
</head>
<body>

<div class="portal-main-heading">
  ID CARD PRINT & CONVERTER PORTAL
</div>

<!-- Contact for Registration Button -->
<div class="top-reg-nav" id="topNavRegistrationBox">
  <button class="top-reg-btn" onclick="openRegModal()">
    💬 Contact for Registration
  </button>
</div>

<!-- 1. Login Screen with Running Ticker, Ad Images & Services Info -->
<div id="loginScreen" class="auth-box">
  
  <!-- Running Ticker Notification -->
  <div class="ticker-container">
    <div class="ticker-text">
      🚀 Smart & Reliable Print Portal — Fast Operations, Simple Workflow & Daily Business Use! | 📌 Essential Document & Photo Printing Services in One Place!
    </div>
  </div>

  <!-- Advertisement Images -->
  <div class="ad-slider-box">
    <img src="https://images.unsplash.com/photo-1544717305-2782549b5136?w=400&auto=format&fit=crop&q=60" alt="Print Service 1" class="ad-slide-img" title="Photo & Document Print">
    <img src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=400&auto=format&fit=crop&q=60" alt="Print Service 2" class="ad-slide-img" title="Passport Sheet Generator">
    <img src="https://images.unsplash.com/photo-1633158829585-23ba8f7c8caf?w=400&auto=format&fit=crop&q=60" alt="Print Service 3" class="ad-slide-img" title="Government ID Print">
  </div>

  <!-- Portal Services Info List -->
  <div class="services-info-card">
    <h4>⚡ Our Printing Services (उपलब्ध मुख्य सर्विसेज):</h4>
    <ul>
      <li>🔹 5-Cards ID Print (A4)</li>
      <li>🔹 Multi-Unique Passports (1 to 5 Photos)</li>
      <li>🔹 4×6 Photo Sheets</li>
      <li>🔹 PDF Editor — Text, Signature, Image & Highlight</li>
      <li>🔹 PDF Arranger & Merger</li>
      <li>🔹 Custom Image Resizer</li>
      <li>🔹 PDF to JPG & Compressor</li>
    </ul>
  </div>

  <div class="badge">Protected Access</div>
  <h2 style="font-size: 20px; margin-bottom: 6px;">Sign In</h2>
  <p style="font-size: 11px; color: var(--text-muted); margin-bottom: 15px;">Card & Photo Generator Portal</p>

  <input type="email" id="loginEmail" class="login-input" placeholder="ईमेल आईडी दर्ज करें" value="oneplus777000@gmail.com">
  <input type="password" id="loginPass" class="login-input" placeholder="पासवर्ड दर्ज करें">
  <button id="authBtn" class="login-btn">लॉगिन करें</button>
  <div id="errorMsg" class="error-msg">⚠️ गलत ईमेल आईडी या पासवर्ड!</div>
  
  <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; flex-wrap:wrap; margin-top:10px;">
    <span id="goToSignUp" class="auth-link">📝 Create Account</span>
    <span id="goToChangePwd" class="auth-link">🔑 Change Password?</span>
  </div>
</div>

<!-- 2. Sign Up Screen -->
<div id="signUpScreen" class="auth-box" style="display:none;">
  <div class="badge">New Registration</div>
  <h2 style="font-size: 20px; margin-bottom: 6px; color: var(--accent-blue);">Sign Up</h2>
  <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 20px;">अपने अकाउंट को बनाएं और पोर्टल में लॉगिन करें</p>

  <input type="text" id="signUpName" class="login-input" placeholder="पूरा नाम लिखें">
  <input type="email" id="signUpEmail" class="login-input" placeholder="ईमेल आईडी दर्ज करें">
  <input type="password" id="signUpPass" class="login-input" placeholder="पासवर्ड बनाएं">
  <input type="password" id="signUpConfirmPass" class="login-input" placeholder="पासवर्ड फिर से लिखें">

  <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 12px; padding: 12px; margin: 12px 0; text-align: left; font-size: 12px; color: var(--text-muted);">
    <div style="font-size: 11px; color: var(--accent-blue); font-weight: 700; margin-bottom: 6px;">💳 QR Payment Instructions</div>
    <div style="margin-bottom: 8px;">Please pay only through the QR code below and upload the proof after payment.</div>

    <div style="display:flex; flex-direction:column; gap:8px; margin-bottom:10px;">
      <label style="display:flex; align-items:center; gap:8px; color:#f8fafc;">
        <input type="radio" name="planType" value="1month" checked>
        <span>1 Month Plan — ₹36</span>
      </label>
      <label style="display:flex; align-items:center; gap:8px; color:#f8fafc;">
        <input type="radio" name="planType" value="1year">
        <span>1 Year Plan — ₹319</span>
      </label>
    </div>

    <div id="paymentQrPlanText" style="margin-bottom: 8px; color: #f8fafc; font-weight: 600;">QR Code for 1 Month Plan (₹36):</div>
    <div style="background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 10px; padding: 12px; text-align: center;">
      <a id="paymentLinkButton" class="payment-link-btn" href="https://i.ibb.co/LWVdcR0/qr-1month-36-png.jpg" target="_blank" rel="noopener noreferrer">💳 Open ₹36 Payment Link</a>
      <img id="paymentQrImage" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAyAAAAMgAQAAAADzCzvFAAAD5UlEQVR4nO3dUW7iMBDG8W82SOlbuIF7E3qzwM3Ym8ANyFuRoLMPxlk7BJalZZdG/3lAqWv4SX4aTTy2uR4fP/6BAQICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAnJHeBbLsQnB3d036WEnSWrc3yVJdXoYhOW/O53lAgEBAQEBAQH5MqT1ItaSpK3Za5rQpNSrdveUdFXltz7+gDwkQEBAQEBAQEC+HbKyU7ylkeC+kbZmc6kzC+47aW9mZi9pzjF9a+QXJ71cICAgICAgICBPhMxunBdckjorBuvR95jnMZ3lAgEBAQEBAQF5LBJfZsaiWh+1e5cV1T6NfDZAQEBAQEBAQJ4bGal3te1wJLi2puDq5mp2v8fr7PjY6spRstNZLhAQEBAQEBCQ++OWpslN+ow79+NnbJekaRIEBAQEBAQE5IkQ+6trlWJRrZtLt+8g05SWCwQEBAQEBATka5CV2VJamb1JP9Pnq6TyUIw+9mVnZnwx6ufNmRNdLhAQEBAQEBCQu5HW3cyW2cjCfZP92bgPtvDHczFmUuV+kI6ciAECAgICAgICciHKs1tH9pGFMvWK0WR7x+JRsIdyApvIQEBAQEBAQED+AzJM7mJ+t0gH+y+y9oCQDvZXSu76JoFDdsL/xyCzI7kDAQEBAQEBAZF01pnZptuUFukhZBN2UpMeznsyL6Ze01kuEBAQEBAQEJD7Y/Rl5iIb2UjK7hBvyvmD6yz7V5rkXSAgICAgICAgV5CVndKldRqJTZMhZV+N+07qsv37fdUrXmdZp3rXZeRRAQICAgICAgICMlZUa9PLzHXWmZnnd3k5rW8PqPxyTGe5QEBAQEBAQEDuj/Oka5lt3o8R0ub9/H3m+QGwbCIDAQEBAQEBAbkSV8pUfWwkjTVNKtW7+pLXQTLyLhAQEBAQEBCQsRjUu84jZKlXjCZLwOImsur6eRXTWS4QEBAQEBAQkO+FtGU5bZ3GQ3ZXeVee8F+XZ8y6WTVoEpjucoGAgICAgICAfAZZ2Sne0sjWzMwW7luzfitZLKft0+TZlRstJ71cICAgICAgICBfiISxm5X2Zk22g0zZJjKn3gUCAgICAgICMozZLZO2r6eHxiWpm58e9qb6XZIq13EmSceZ7EP+Q5YnXtNZLhAQEBAQEBCQ50ZGkru2HY4El6StSVKzS5ndy+m/8aHy06ebzMvvT2e5QEBAQEBAQEDuj1s6MzfpuSlvVnrPTsToI1bT6MwEAQEBAQEBASljWJp6SExnuUBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQKaF/ALDGkmmOVEHeQAAAABJRU5ErkJggg==" alt="Payment QR Code for ₹36" style="max-width: 220px; width: 100%; height: auto; display: block; visibility: visible; opacity: 1; margin: 0 auto; background: #fff; padding: 8px; border-radius: 10px; border: 1px solid rgba(15, 23, 42, 0.15); box-shadow: 0 4px 12px rgba(0,0,0,0.18);">
      <div id="paymentQrNote" style="margin-top: 8px; font-size: 11px; color: var(--text-muted);">This QR is for the ₹36 plan.</div>
    </div>
  </div>

  <input type="text" id="signUpTxnId" class="login-input" placeholder="Transaction ID / Reference Number">
  <label style="display:block; width:100%; text-align:left; font-size:11px; color:var(--text-muted); margin-bottom:8px;">📸 Upload payment screenshot</label>
  <input type="file" id="signUpPaymentScreenshot" accept="image/jpeg,image/jpg,image/png,image/webp" style="display:block; width:100%; background: rgba(15, 23, 42, 0.9); color:#fff; padding:10px; border-radius:10px; border:1px solid rgba(56, 189, 248, 0.3); margin-bottom:12px;">

  <button id="signUpBtn" class="login-btn" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);">✅ Create Account</button>
  <div id="signUpStatusMsg" style="font-size:13px; margin-top:12px; display:none; font-weight:500;"></div>

  <div>
    <span id="backToLoginFromSignUp" class="auth-link">⬅️ Already have account? Login</span>
  </div>
</div>

<!-- Expired Distributor Renewal Screen -->
<div id="renewalScreen" class="auth-box" style="display:none;">
  <div class="badge" style="color:#fbbf24; border-color:rgba(245,158,11,.4); background:rgba(245,158,11,.15);">Renewal Required</div>
  <h2 style="font-size:20px; margin-bottom:6px; color:#fbbf24;">🔄 Renew Your Portal</h2>
  <p id="renewalGreeting" style="font-size:12px; color:var(--text-muted); margin-bottom:16px;">आपकी validity समाप्त हो चुकी है। अपना plan चुनकर payment पूरा करें।</p>
  <div style="background:rgba(15,23,42,.9); border:1px solid rgba(56,189,248,.35); border-radius:12px; padding:12px; margin-bottom:12px; text-align:left; font-size:12px;">
    <label style="display:flex; align-items:center; gap:8px; margin-bottom:9px;"><input type="radio" name="renewalPlanType" value="1month"><span>1 Month Renewal — ₹36</span></label>
    <label style="display:flex; align-items:center; gap:8px;"><input type="radio" name="renewalPlanType" value="1year"><span>1 Year Renewal — ₹319</span></label>
    <a id="renewalPaymentLink" class="payment-link-btn" href="#" target="_blank" rel="noopener noreferrer" style="margin-top:12px;">💳 Open Payment Link</a>
  </div>
  <input type="text" id="renewalTxnId" class="login-input" placeholder="Transaction ID / Reference Number">
  <label style="display:block; width:100%; text-align:left; font-size:11px; color:var(--text-muted); margin-bottom:8px;">📸 Upload payment screenshot</label>
  <input type="file" id="renewalPaymentScreenshot" accept="image/jpeg,image/jpg,image/png,image/webp" style="display:block; width:100%; background:rgba(15,23,42,.9); color:#fff; padding:10px; border-radius:10px; border:1px solid rgba(56,189,248,.3); margin-bottom:12px;">
  <button id="submitRenewalBtn" class="login-btn" style="background:linear-gradient(135deg,#f59e0b 0%,#d97706 100%);">📤 Submit Renewal for Approval</button>
  <div id="renewalStatusMsg" style="font-size:13px; margin-top:12px; display:none; font-weight:500;"></div>
  <div><span id="backToLoginFromRenewal" class="auth-link">⬅️ Back to Login</span></div>
</div>


<div id="pendingScreen" class="auth-box" style="display:none;">
  <h2>Payment Review</h2>
  <p id="pendingStatus"></p>
  <p>Your portal remains locked until admin approval. If your signup screenshot failed, upload it here.</p>
  <input id="pendingScreenshot" type="file" accept="image/jpeg,image/png,image/webp">
  <button id="pendingUploadBtn" class="login-btn">Upload Signup Screenshot</button>
  <button id="pendingBackBtn" class="login-btn">Back to Login</button>
</div>


<div id="adminUnlockModal" role="dialog" aria-modal="true" aria-labelledby="adminUnlockTitle" style="display:none;position:fixed;inset:0;z-index:10000;background:rgba(0,0,0,.8);align-items:center;justify-content:center;">
 <form id="adminUnlockForm" class="auth-box" style="margin:20px;max-width:400px;">
  <h2 id="adminUnlockTitle">🔒 Unlock Admin Panel</h2>
  <p>Admin Panel खोलने के लिए अपना मौजूदा admin login password दोबारा डालें।</p>
  <input id="adminUnlockPassword" type="password" class="login-input" placeholder="Admin password" autocomplete="current-password" required maxlength="128" aria-label="Admin panel password">
  <p id="adminUnlockError" role="alert" style="color:#f87171;"></p>
  <button id="adminUnlockSubmit" type="submit" class="login-btn">Unlock Panel</button>
  <button id="adminUnlockCancel" type="button" class="login-btn" style="background:#475569;">Cancel</button>
  <p style="font-size:12px;">Panel छोड़ने पर या 5 मिनट बाद फिर lock होगा।</p>
 </form>
</div>

<!-- 3. Change Password Screen -->
<div id="changePwdScreen" class="auth-box" style="display:none;">
  <div class="badge">Security Settings</div>
  <h2 style="font-size: 20px; margin-bottom: 6px; color: var(--accent-blue);">🔑 Change Password</h2>
  <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 20px;">ईमेल आईडी, पुराना और नया पासवर्ड दर्ज करें</p>

  <input type="email" id="pwdEmailInput" class="login-input" placeholder="अपनी ईमेल आईडी (Login Email)">
  <input type="password" id="oldPassInput" class="login-input" placeholder="पुराना पासवर्ड">
  <input type="password" id="newPassInput" class="login-input" placeholder="नया पासवर्ड">
  <input type="password" id="confirmPassInput" class="login-input" placeholder="नया पासवर्ड कन्फर्म करें">
  
  <button id="saveNewPwdBtn" class="login-btn" style="background: var(--btn-download);">💾 नया पासवर्ड सेव करें</button>
  <div id="pwdStatusMsg" style="font-size:13px; margin-top:12px; display:none; font-weight:500;"></div>

  <div>
    <span id="backToLogin" class="auth-link">⬅️ Back to Login</span>
  </div>
</div>

<!-- 3. Main Portal Application -->
<div id="mainApp">
  <div class="tab-nav">
    <button class="tab-btn active" onclick="switchTab('tab-cards')">💳 ID Card (5 Slots)</button>
    <button class="tab-btn" onclick="switchTab('tab-passport')">👤 Passport Photos</button>
    <button class="tab-btn" onclick="switchTab('tab-name-passport')">📝 Name & Date Passport</button>
    <button class="tab-btn" onclick="switchTab('tab-4x6')">🖼️ 4×6 Photo Print</button>
    <button class="tab-btn" onclick="switchTab('tab-pdf-editor')">✏️ PDF Editor</button>
    <button class="tab-btn" onclick="switchTab('tab-arranger')">📑 PDF Arranger</button>
    <button class="tab-btn" onclick="switchTab('tab-jpg-to-pdf')">📄 PDF, JPG, PNG to PDF</button>
    <button class="tab-btn" onclick="switchTab('tab-resizer')">📐 Image Resizer</button>
    <button class="tab-btn" onclick="switchTab('tab-pdf-to-jpg')">🖼️ PDF to JPG (Manual DPI)</button>
    <button class="tab-btn" onclick="switchTab('tab-pdf-compressor')">🗜️ PDF Compressor</button>
    <button class="tab-btn" onclick="switchTab('tab-history')" style="border-color: rgba(56, 189, 248, 0.5);">📂 History</button>
    <button id="adminTabBtn" class="tab-btn" onclick="switchTab('tab-admin')" style="display:none; border-color: #f59e0b; color:#fbbf24;">⚙️ Admin Panel</button>
  </div>

  <div class="container">
    <!-- Top Header Bar with Live Validity Counter & Logout -->
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; flex-wrap: wrap; gap: 10px;">
      <div id="validityCounterBadge" style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10b981; color: #34d399; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 600;">
        ⏳ Validity: Initializing...
      </div>
      <button id="logoutBtn" class="logout-btn">🔒 Logout</button>
    </div>

    <!-- Distributor Notification Banner with QR/Image & Reply Payment Screenshot Option -->
    <div id="distributorNoticeBanner" style="display:none; background: rgba(245, 158, 11, 0.2); border: 1px solid #fbbf24; color: #fef08a; padding: 14px 18px; border-radius: 12px; margin-bottom: 15px; font-size: 13px; text-align: left;">
      <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 15px; flex-wrap: wrap;">
        <div style="flex: 1; min-width: 240px;">
          <strong>📢 Admin Notice / QR Code:</strong>
          <div id="distributorNoticeText" style="margin-top: 4px; font-weight: 500;"></div>
          <div id="distributorNoticeImgBox" style="margin-top: 10px; display:none;">
            <img id="distributorNoticeImg" src="" style="max-width: 100%; max-height: 220px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.3);" alt="QR / Banner">
          </div>
        </div>

        <!-- Reply Message & Screenshot Box for Distributor -->
        <div style="background: rgba(15,23,42,0.85); border: 1px solid rgba(56,189,248,0.4); padding: 12px; border-radius: 10px; min-width: 220px; text-align: center;">
          <div style="font-size: 11px; color: var(--accent-blue); margin-bottom: 6px; font-weight: 600;">💬 Reply to Admin</div>
          <textarea id="distReplyMessage" placeholder="अपना जवाब लिखें..." style="display:block; width:100%; min-height:58px; resize:vertical; background:#0f172a; color:#fff; padding:7px; font-size:11px; border-radius:6px; border:1px solid rgba(56,189,248,0.4); margin-bottom:8px;"></textarea>
          <input type="file" id="distScreenshotInput" accept="image/jpeg,image/jpg,image/png,image/webp" style="display:block; width:100%; background:#334155; color:#fff; padding:6px; font-size:11px; border-radius:6px; border:1px solid rgba(56,189,248,0.4); margin-bottom:8px; cursor:pointer;">
          <button onclick="sendDistributorReply()" class="action-btn btn-download" style="padding: 6px 12px; font-size: 11px; width: 100%;">📤 Send Reply</button>
          <div id="screenshotUploadStatus" style="font-size:10px; margin-top:4px; display:none;"></div>
        </div>
      </div>
    </div>

    <!-- TAB 1: 5 CARDS SYSTEM -->
    <div id="tab-cards" class="tab-content active">
      <div class="badge">Auto-Dimension Crop • 2.5mm Gap • Broad Black Border • 5 Cards</div>
      <h1>Card Generator System</h1>
      <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 10px;">इमेज सिलेक्ट करते ही वह <strong>ऑटोमैटिकली सही ID साइज में फिट</strong> हो जाएगी। जरूरत पड़ने पर मैनुअल क्रॉप भी कर सकते हैं।</p>
      
      <div id="slotCounter" class="slot-counter-badge">Cards on Page: 0 / 5 (Next Slot: #1)</div>

      <div class="upload-section">
        <label class="upload-box" for="card1Input">
          <strong style="display:block; font-size:14px; margin-bottom:4px;">📁 Front Side</strong>
          <div id="file1Name" style="font-size: 12px; color: var(--text-muted);">इमेज चुनें (Auto-Crop)</div>
        </label>
        <input type="file" id="card1Input" accept="image/*">

        <label class="upload-box" for="card2Input">
          <strong style="display:block; font-size:14px; margin-bottom:4px;">📁 Back Side</strong>
          <div id="file2Name" style="font-size: 12px; color: var(--text-muted);">इमेज चुनें (Auto-Crop)</div>
        </label>
        <input type="file" id="card2Input" accept="image/*">
      </div>

      <div class="preview-container">
        <div class="preview-box">
          <h4>Front Card Preview</h4>
          <canvas id="canvas1" width="1013" height="638" style="width: 180px;"></canvas>
          <button id="manualCropFrontBtn" class="btn-manual-crop" style="display:none;" onclick="openManualCropForCard('front')">✂️ Manual Crop Front</button>
        </div>
        <div class="preview-box">
          <h4>Back Card Preview</h4>
          <canvas id="canvas2" width="1013" height="638" style="width: 180px;"></canvas>
          <button id="manualCropBackBtn" class="btn-manual-crop" style="display:none;" onclick="openManualCropForCard('back')">✂️ Manual Crop Back</button>
        </div>
      </div>

      <div class="btn-group">
        <button id="addCardBtn" class="action-btn btn-add" disabled>➕ Add This Card to A4 Sheet</button>
        <button id="resetPageBtn" class="action-btn btn-reset">🔄 Clear A4 Page</button>
      </div>

      <div style="margin-top: 25px; border-top: 1px solid var(--border-color); padding-top: 15px;">
        <h3 style="font-size: 15px; color: var(--accent-blue); margin-bottom: 6px;">A4 Sheet Preview</h3>
        <div style="display:inline-block; max-width: 250px; background:#fff; border-radius:6px; overflow:hidden; border: 1px solid #475569;">
          <canvas id="a4Canvas" width="2480" height="3508" style="width: 100%; display:block;"></canvas>
        </div>
        <div class="btn-group">
          <button id="downloadPdfBtn" class="action-btn btn-download" disabled>📥 Direct A4 PDF Download</button>
        </div>
      </div>
    </div>

    <!-- TAB 2: PASSPORT SIZE PHOTOS (MULTI-UNIQUE PHOTOS & GENERATE/DOWNLOAD FLOW) -->
    <div id="tab-passport" class="tab-content">
      <div class="badge">Standard 35mm × 45mm • Multi-Unique Photo Generator & Custom Qty</div>
      <h1>Passport Photo Generator</h1>
      <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 12px;">1 से 5 अलग-अलग फ़ोटो चुनें, संख्या सेट करें, पहले 'Generate' करके प्रीव्यू देखें और फिर डाउनलोड करें:</p>

      <!-- Multi-Photo Buttons Selector (1 to 5 Photos) -->
      <div class="control-panel" style="margin-bottom: 12px;">
        <span style="font-size: 13px; font-weight:600; color: var(--accent-blue);">📂 Select Unique Photos Mode (1 to 5 Photos):</span>
        <div class="qty-select-group" style="margin-top: 8px;">
          <button class="quick-qty-btn" id="btnCount1" onclick="setPassportCount(1)" style="background:#0284c7;">1 Photo</button>
          <button class="quick-qty-btn" id="btnCount2" onclick="setPassportCount(2)">2 Photos</button>
          <button class="quick-qty-btn" id="btnCount3" onclick="setPassportCount(3)">3 Photos</button>
          <button class="quick-qty-btn" id="btnCount4" onclick="setPassportCount(4)">4 Photos</button>
          <button class="quick-qty-btn" id="btnCount5" onclick="setPassportCount(5)">5 Photos</button>
        </div>
      </div>

      <!-- Dynamic Upload Blocks Container -->
      <div id="passportUploadBlocksContainer" style="display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; margin-bottom: 12px;">
        <!-- Dynamically rendered via JS -->
      </div>

      <!-- Custom Quantity Control Panel -->
      <div class="control-panel" style="margin-bottom: 15px;">
        <span style="font-size: 13px; font-weight:600; color: var(--accent-blue);">🔢 A4 शीट पर कुल फ़ोटो की संख्या (Quantity) चुनें या टाइप करें:</span>
        <div class="qty-select-group">
          <input type="number" id="passportQtyInput" class="qty-input" value="8" min="1" max="50">
          <button class="quick-qty-btn" onclick="setPassportQty(2)">2</button>
          <button class="quick-qty-btn" onclick="setPassportQty(4)">4</button>
          <button class="quick-qty-btn" onclick="setPassportQty(6)">6</button>
          <button class="quick-qty-btn" onclick="setPassportQty(8)">8</button>
          <button class="quick-qty-btn" onclick="setPassportQty(12)">12</button>
          <button class="quick-qty-btn" onclick="setPassportQty(16)">16</button>
          <button class="quick-qty-btn" onclick="setPassportQty(30)">30</button>
        </div>
      </div>

      <!-- STEP 1: GENERATE BUTTON (UPPER) -->
      <div class="btn-group">
        <button id="generateMultiPassportA4Btn" class="action-btn btn-add">🖼️ Generate Sheet (Preview)</button>
      </div>

      <!-- PREVIEW & STEP 2: DOWNLOAD BUTTON (LOWER) -->
      <div style="margin-top: 25px; border-top: 1px solid var(--border-color); padding-top: 15px;">
        <h3 id="passportSheetTitle" style="font-size: 15px; color: var(--accent-blue); margin-bottom: 6px;">A4 Passport Sheet Preview</h3>
        <div style="display:inline-block; max-width: 250px; background:#fff; border-radius:6px; overflow:hidden; border: 1px solid #475569;">
          <canvas id="passportSheetCanvas" width="2480" height="3508" style="width: 100%; display:block;"></canvas>
        </div>
        <div class="btn-group">
          <button id="downloadMultiPassportPdfBtn" class="action-btn btn-download" disabled>📥 Download A4 Sheet PDF</button>
        </div>
      </div>
    </div>

    <!-- TAB 3: NAME & DATE PASSPORT PHOTO MAKER -->
    <div id="tab-name-passport" class="tab-content">
      <div class="badge">Govt / Exam Standard • 3 Separate Font Sliders • Auto DOB Label</div>
      <h1>Name & Date Passport Photo Maker</h1>
      <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 12px;">नाम, DOB और DOP के लिए अलग-अलग स्लाइडर से फॉन्ट साइज़ कंट्रोल करें।</p>

      <div class="upload-section" style="margin-bottom:10px;">
        <label class="upload-box" for="namePassportInput" style="max-width: 380px;">
          <strong style="display:block; font-size:14px; margin-bottom:4px;">📁 Upload Candidate Photo</strong>
          <div id="namePassportFileName" style="font-size: 12px; color: var(--text-muted);">फ़ोटो चुनें व क्रॉप करें</div>
        </label>
        <input type="file" id="namePassportInput" accept="image/*">
      </div>

      <div class="control-panel" style="text-align:left;">
        <div style="display:flex; flex-direction:column; gap:10px;">
          
          <div style="background:rgba(15,23,42,0.6); padding:8px 12px; border-radius:8px; border:1px solid var(--border-color);">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <label style="font-size:11px; color:var(--text-muted);">👤 Candidate Name:</label>
              <span id="nameFontLabel" style="font-size:11px; color:var(--accent-blue); font-weight:600;">Size: 24px</span>
            </div>
            <input type="text" id="candNameInput" class="text-field-input" style="max-width:100%;" placeholder="e.g. HARSHAL SATISH MARATHE" oninput="renderNamePassportPreview()">
            <input type="range" id="nameFontSlider" class="slider-range" min="14" max="36" value="24" oninput="updateNameFontSize(this.value)">
          </div>

          <div style="background:rgba(15,23,42,0.6); padding:8px 12px; border-radius:8px; border:1px solid var(--border-color);">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <label style="font-size:11px; color:var(--text-muted);">🎂 Date of Birth (DOB):</label>
              <span id="dobFontLabel" style="font-size:11px; color:var(--accent-blue); font-weight:600;">Size: 20px</span>
            </div>
            <input type="text" id="candDobInput" class="text-field-input" style="max-width:100%;" placeholder="e.g. 15/08/1998" oninput="renderNamePassportPreview()">
            <input type="range" id="dobFontSlider" class="slider-range" min="12" max="30" value="20" oninput="updateDobFontSize(this.value)">
          </div>

          <div style="background:rgba(15,23,42,0.6); padding:8px 12px; border-radius:8px; border:1px solid var(--border-color);">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <label style="font-size:11px; color:var(--text-muted);">📅 Photo Date (DOP):</label>
              <span id="dopFontLabel" style="font-size:11px; color:var(--accent-blue); font-weight:600;">Size: 20px</span>
            </div>
            <input type="text" id="candDopInput" class="text-field-input" style="max-width:100%;" placeholder="DOP: DD/MM/YYYY" oninput="renderNamePassportPreview()">
            <input type="range" id="dopFontSlider" class="slider-range" min="12" max="30" value="20" oninput="updateDopFontSize(this.value)">
          </div>

        </div>

        <div style="margin-top:12px; text-align:center;">
          <span style="font-size: 12px; font-weight:600; color: var(--accent-blue);">🔢 फ़ोटो संख्या:</span>
          <input type="number" id="namePassportQtyInput" class="qty-input" value="8" min="1" max="30">
          <button class="quick-qty-btn" onclick="setNamePassportQty(4)">4</button>
          <button class="quick-qty-btn" onclick="setNamePassportQty(6)">6</button>
          <button class="quick-qty-btn" onclick="setNamePassportQty(8)">8</button>
          <button class="quick-qty-btn" onclick="setNamePassportQty(12)">12</button>
          <button class="quick-qty-btn" onclick="setNamePassportQty(30)">30</button>
        </div>
      </div>

      <div class="preview-container">
        <div class="preview-box">
          <h4>Preview with Name & Date Strip</h4>
          <canvas id="namePassportCanvas" width="413" height="531" style="width: 155px;"></canvas>
        </div>
      </div>

      <div class="btn-group">
        <button id="make4x6NamePassportBtn" class="action-btn btn-add" disabled>🖼️ Generate 4×6 Sheet</button>
        <button id="makeA4NamePassportBtn" class="action-btn btn-add" disabled>📄 Generate A4 Sheet</button>
      </div>

      <div style="margin-top: 20px; border-top: 1px solid var(--border-color); padding-top: 15px;">
        <h3 id="namePassportSheetTitle" style="font-size: 15px; color: var(--accent-blue); margin-bottom: 6px;">Sheet Preview</h3>
        <div style="display:inline-block; max-width: 250px; background:#fff; border-radius:6px; overflow:hidden; border: 1px solid #475569;">
          <canvas id="namePassportSheetCanvas" width="1800" height="1200" style="width: 100%; display:block;"></canvas>
        </div>
        <div class="btn-group">
          <button id="downloadNamePassportPdfBtn" class="action-btn btn-download" disabled>📥 Download Name & Date Sheet PDF</button>
        </div>
      </div>
    </div>

    <!-- TAB 4: 4x6 PHOTO PRINT -->
    <div id="tab-4x6" class="tab-content">
      <div class="badge">Clear 300 DPI • 1200 × 1800 px • Max 4 Photos</div>
      <h1>4×6 Photo Print Generator</h1>
      <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 15px;">4×6 इंच फ़ोटो अपलोड करें, 1 से 4 तक संख्या चुनें और A4 या 4×6 शीट PDF निकालें।</p>

      <div class="upload-section">
        <label class="upload-box" for="photo4x6Input" style="max-width: 380px;">
          <strong style="display:block; font-size:14px; margin-bottom:4px;">📁 4×6 Photo Upload</strong>
          <div id="photo4x6FileName" style="font-size: 12px; color: var(--text-muted);">फ़ोटो चुनें व क्रॉप करें</div>
        </label>
        <input type="file" id="photo4x6Input" accept="image/*">
      </div>

      <div class="preview-container">
        <div class="preview-box">
          <h4>Cropped 4×6 Photo Canvas</h4>
          <canvas id="canvas4x6" width="1200" height="1800" style="width: 150px;"></canvas>
        </div>
      </div>

      <div class="control-panel">
        <span style="font-size: 14px; font-weight:600; color: var(--accent-blue);">🔢 A4 शीट पर 4×6 फ़ोटो की संख्या चुनें (Max 4):</span>
        <div class="qty-select-group">
          <input type="number" id="photo4x6QtyInput" class="qty-input" value="2" min="1" max="4">
          <button class="quick-qty-btn" onclick="set4x6Qty(1)">1 Photo</button>
          <button class="quick-qty-btn" onclick="set4x6Qty(2)">2 Photos</button>
          <button class="quick-qty-btn" onclick="set4x6Qty(3)">3 Photos</button>
          <button class="quick-qty-btn" onclick="set4x6Qty(4)">4 Photos</button>
        </div>
      </div>

      <div class="btn-group">
        <button id="downloadDirect4x6Pdf" class="action-btn btn-download" disabled>📥 Direct 1 Photo (4×6 Paper PDF)</button>
        <button id="generateA4Custom4x6Btn" class="action-btn btn-add" disabled>📄 Generate Selected Qty on A4 Sheet</button>
      </div>

      <div style="margin-top: 25px; border-top: 1px solid var(--border-color); padding-top: 15px;">
        <h3 id="photo4x6SheetTitle" style="font-size: 15px; color: var(--accent-blue); margin-bottom: 6px;">A4 4×6 Photo Sheet Preview</h3>
        <div style="display:inline-block; max-width: 250px; background:#fff; border-radius:6px; overflow:hidden; border: 1px solid #475569;">
          <canvas id="a4_4x6_SheetCanvas" width="2480" height="3508" style="width: 100%; display:block;"></canvas>
        </div>
        <div class="btn-group">
          <button id="downloadA4_4x6_PdfBtn" class="action-btn btn-download" disabled>📥 Download A4 4×6 Sheet PDF</button>
        </div>
      </div>
    </div>

<div id="tab-pdf-editor" class="tab-content">
 <section class="pe-shell" aria-label="PDF Editor">
  <header class="pe-heading"><div><span class="pe-eyebrow">DOCUMENT TOOLS</span><h1>PDF Editor</h1><p>Text, signatures और images जोड़ें — आपकी PDF इसी browser में रहती है।</p></div><button id="pe-download" class="pe-primary" disabled>↓ Download PDF</button></header>
  <div class="pe-filebar"><button id="pe-open" class="pe-primary">＋ Open PDF</button><input id="pe-file" type="file" accept="application/pdf,.pdf" hidden><span id="pe-filename">कोई PDF नहीं चुनी है · अधिकतम 50 MB / 150 pages</span><button id="pe-close" disabled>Close document</button></div>
  <p class="pe-notice">यह annotation editor है। पुराने text को बदलने के लिए Whiteout + Text लगाएँ। <strong>Whiteout सुरक्षित redaction नहीं है:</strong> मूल text PDF में रहता है। OCR / मूल text editing उपलब्ध नहीं है।</p>
  <fieldset id="pe-controls" disabled>
   <div class="pe-toolbar" role="toolbar" aria-label="Editing tools">
    <button data-pe-tool="select" aria-pressed="true">↖ Select / Move</button><button data-pe-tool="text" aria-pressed="false">T Text</button><button data-pe-tool="draw" aria-pressed="false">✎ Draw / Sign</button><button data-pe-tool="highlight" aria-pressed="false">▰ Highlight</button><button data-pe-tool="whiteout" aria-pressed="false">▱ Whiteout</button><button data-pe-tool="rect" aria-pressed="false">□ Rectangle</button><button data-pe-tool="check" aria-pressed="false">✓ Check</button><button data-pe-tool="cross" aria-pressed="false">✕ Cross</button><button id="pe-image">▧ Image / Signature</button><input id="pe-image-file" type="file" accept="image/png,image/jpeg" hidden>
   </div>
   <div class="pe-options"><label>Color <input id="pe-color" type="color" value="#111827"></label><label>Text size <input id="pe-size" type="number" value="18" min="6" max="120"></label><label>Pen width <input id="pe-pen" type="number" value="2" min="1" max="20"></label><label><input id="pe-bold" type="checkbox"> Bold</label><button id="pe-undo" disabled>↶ Undo</button><button id="pe-redo" disabled>↷ Redo</button></div>
   <div class="pe-workspace">
    <aside class="pe-sidebar"><h3>Text & selection</h3><label for="pe-text">Text to place / selected text</label><textarea id="pe-text" rows="4" maxlength="2000" placeholder="यहाँ text लिखें, Text चुनें और page पर click करें…"></textarea><button id="pe-apply">Apply text / style</button><p>Select / Move से अपने जोड़े हुए item को चुनकर खिसकाएँ।</p><div class="pe-row"><button id="pe-smaller">− Smaller</button><button id="pe-larger">＋ Larger</button></div><button id="pe-delete" class="pe-danger">Delete selected</button><div id="pe-selection" class="pe-muted">No item selected</div><hr><h3>How to use</h3><p>Text / ✓ / ✕: page पर click करें।<br>Draw / Highlight / Whiteout / Rectangle: click करके drag करें।<br>Image: PNG/JPG चुनें, फिर page पर click करें।</p><p>Signature केवल drawing/image है; digital certificate नहीं है।</p></aside>
    <div class="pe-document"><div class="pe-pagination"><button id="pe-prev" aria-label="Previous page">←</button><label>Page <select id="pe-page" aria-label="Page"></select></label><span id="pe-count">/ 0</span><button id="pe-next" aria-label="Next page">→</button><label>Zoom <select id="pe-zoom"><option value="0.75">75%</option><option value="1" selected>100%</option><option value="1.25">125%</option><option value="1.5">150%</option></select></label></div><div id="pe-scroll"><div id="pe-empty"><span>▤</span><h2>Your PDF workspace</h2><p>Open PDF दबाएँ और editing शुरू करें।<br>कोई file server पर upload नहीं होगी।</p></div><div id="pe-page-wrap" hidden><canvas id="pe-base"></canvas><canvas id="pe-overlay" aria-label="PDF editing canvas"></canvas></div></div></div>
   </div>
  </fieldset>
  <div id="pe-status" role="status" aria-live="polite">Ready · PDF libraries लोड करने के लिए internet चाहिए।</div>
 </section>
</div>

    <!-- TAB 5: PDF ARRANGER (DRAG & DROP / HOLD & MOVE) -->
    <div id="tab-arranger" class="tab-content">
      <div class="badge">Drag & Drop To Re-order • Hold & Move • Rotate 90° • Cut Pages</div>
      <h1>PDF Page Arranger & Organizer</h1>
      <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 12px;">किसी भी पेज को <strong>पकड़कर (Hold करके) मनचाही जगह पर सरकाएँ</strong>।</p>

      <div class="upload-section" style="margin-bottom: 15px;">
        <label class="upload-box" for="arrangerPdfInput" style="max-width: 420px;">
          <strong style="display:block; font-size:14px; margin-bottom:4px; color:var(--accent-blue);">📑 Select / Add PDF to Arrange</strong>
          <div id="arrangerStatus" style="font-size: 12px; color: var(--text-muted);">क्लिक करके .pdf फाइल अपलोड करें</div>
        </label>
        <input type="file" id="arrangerPdfInput" accept="application/pdf" multiple>
      </div>

      <div id="arrangerContainerArea" style="display:none;">
        <div style="display:flex; justify-content:space-between; align-items:center; max-width:900px; margin:0 auto 10px auto;">
          <span style="font-size: 13px; font-weight:600; color: var(--accent-blue);">Total Pages: <strong id="arrangerTotalPagesCount" style="color:#fbbf24;">0</strong></span>
          <label for="arrangerPdfInput" class="action-btn btn-add" style="padding:6px 14px; font-size:11px; cursor:pointer;">➕ Add More PDF Files</label>
        </div>

        <div id="arrangerGridList" class="file-gallery-list"></div>

        <div class="btn-group">
          <button id="saveArrangedPdfBtn" class="action-btn btn-download">💾 Save & Download Arranged PDF</button>
          <button id="clearArrangerBtn" class="action-btn btn-reset">🔄 Clear All Pages</button>
        </div>
      </div>
    </div>

    <!-- TAB 6: UNIVERSAL MERGE & RE-ORDER -->
    <div id="tab-jpg-to-pdf" class="tab-content">
      <div class="badge">Universal File Merger • Drag & Drop Re-order • Individual Delete</div>
      <h1>PDF, JPG, PNG to PDF Converter</h1>
      <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 12px;">फ़ाइलों को <strong>माउस से पकड़कर आगे-पीछे क्रमबद्ध करें</strong> और कंबाइंड PDF बनाएँ।</p>

      <div class="upload-section" style="margin-bottom: 15px;">
        <label class="upload-box" for="universalMultiInput" style="max-width: 450px;">
          <strong style="display:block; font-size:14px; margin-bottom:4px; color:var(--accent-blue);">📁 Select Files (PDF, JPG, PNG Allowed)</strong>
          <div id="universalMultiStatus" style="font-size: 12px; color: var(--text-muted);">क्लिक करके PDF या इमेज फ़ाइलें चुनें</div>
        </label>
        <input type="file" id="universalMultiInput" accept="image/jpeg,image/png,image/jpg,application/pdf" multiple>
      </div>

      <div id="universalGalleryContainer" style="display:none;">
        <div style="font-size: 12px; color: var(--accent-blue); font-weight: 600; margin-bottom: 6px;">
          Selected Files (<span id="universalSelectedCount">0</span>):
        </div>
        <div id="universalGalleryList" class="file-gallery-list"></div>

        <div class="btn-group">
          <button id="convertUniversalToPdfBtn" class="action-btn btn-download">📥 Convert & Download Combined PDF</button>
          <button id="clearUniversalListBtn" class="action-btn btn-reset">🔄 Clear All</button>
        </div>
      </div>
    </div>

    <!-- TAB 7: CUSTOM IMAGE RESIZER -->
    <div id="tab-resizer" class="tab-content">
      <div class="badge">Resize in Pixels (px) • Millimeters (mm) • Centimeters (cm)</div>
      <h1>Custom Image Resizer</h1>
      <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 12px;">किसी भी इमेज को अपनी ज़रूरत के अनुसार Width और Height (px, mm, cm) में रीसाइज़ करें।</p>

      <div class="upload-section" style="margin-bottom: 15px;">
        <label class="upload-box" for="resizerImageInput" style="max-width: 400px;">
          <strong style="display:block; font-size:14px; margin-bottom:4px; color:var(--accent-blue);">📁 Select Image to Resize</strong>
          <div id="resizerFileName" style="font-size: 12px; color: var(--text-muted);">क्लिक करके इमेज चुनें (JPG / PNG)</div>
        </label>
        <input type="file" id="resizerImageInput" accept="image/*">
      </div>

      <div id="resizerControlsPanel" style="display:none;">
        <div class="control-panel" style="text-align:left;">
          <div style="display:flex; flex-wrap:wrap; gap:12px; justify-content:center; align-items:center;">
            <div>
              <label style="font-size:11px; color:var(--text-muted); display:block; margin-bottom:3px;">📏 Unit (इकाई):</label>
              <select id="resizerUnitSelect" class="text-field-input" style="max-width:110px;" onchange="onResizerUnitChange()">
                <option value="px" selected>Pixels (px)</option>
                <option value="mm">Millimeters (mm)</option>
                <option value="cm">Centimeters (cm)</option>
              </select>
            </div>
            <div>
              <label style="font-size:11px; color:var(--text-muted); display:block; margin-bottom:3px;">↔️ Width (चौड़ाई):</label>
              <input type="number" id="resizerWidthInput" class="qty-input" style="width:100px;" value="300" oninput="onResizerDimensionChange('width')">
            </div>
            <div>
              <label style="font-size:11px; color:var(--text-muted); display:block; margin-bottom:3px;">↕️ Height (ऊंचाई):</label>
              <input type="number" id="resizerHeightInput" class="qty-input" style="width:100px;" value="300" oninput="onResizerDimensionChange('height')">
            </div>
          </div>

          <div style="margin-top:10px; display:flex; justify-content:center; align-items:center; gap:15px; font-size:12px; color:var(--text-muted);">
            <label style="cursor:pointer; display:flex; align-items:center; gap:5px;">
              <input type="checkbox" id="resizerAspectLock"> Lock Aspect Ratio (अनुपात लॉक रखें)
            </label>
            <span style="color:var(--accent-blue);">DPI: 300 (for mm/cm)</span>
          </div>
        </div>

        <div class="preview-container">
          <div class="preview-box">
            <h4>Resized Output Preview</h4>
            <canvas id="resizerPreviewCanvas" style="max-width: 250px; max-height: 250px;"></canvas>
            <div id="resizerOutputInfo" style="font-size:11px; color:var(--accent-blue); margin-top:5px;">0 x 0 px</div>
          </div>
        </div>

        <div class="btn-group">
          <button id="downloadResizedJpgBtn" class="action-btn btn-download">📥 Download JPG Image</button>
          <button id="downloadResizedPngBtn" class="action-btn btn-add">📥 Download PNG Image</button>
        </div>
      </div>
    </div>

    <!-- TAB 8: PDF TO HIGH-DPI JPG CONVERTER -->
    <div id="tab-pdf-to-jpg" class="tab-content">
      <div class="badge">Ultra High-Res • Manual & Quick DPI (72 to 1200 DPI) • Batch ZIP Export</div>
      <h1>PDF to High-DPI JPG Converter</h1>
      <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 12px;">PDF फ़ाइल अपलोड करें और अपनी आवश्यकतानुसार DPI रिज़ॉल्यूशन टाइप या सेलेक्ट करें।</p>

      <div class="upload-section" style="margin-bottom: 15px;">
        <label class="upload-box" for="pdfToJpgInput" style="max-width: 420px;">
          <strong style="display:block; font-size:14px; margin-bottom:4px; color:var(--accent-blue);">📄 Select PDF File to Convert</strong>
          <div id="pdfToJpgStatus" style="font-size: 12px; color: var(--text-muted);">क्लिक करके .pdf फाइल चुनें</div>
        </label>
        <input type="file" id="pdfToJpgInput" accept="application/pdf">
      </div>

      <div id="pdfToJpgControls" style="display:none;">
        <div class="control-panel">
          <span style="font-size: 13px; font-weight:600; color: var(--accent-blue);">⚙️ Quick Select or Type Custom DPI (Max 1200):</span>
          <div class="qty-select-group">
            <button class="quick-qty-btn" onclick="setPdfDpi(72)">72 DPI</button>
            <button class="quick-qty-btn" onclick="setPdfDpi(150)">150 DPI</button>
            <button class="quick-qty-btn" onclick="setPdfDpi(300)">300 DPI</button>
            <button class="quick-qty-btn" onclick="setPdfDpi(600)">600 DPI</button>
            <button class="quick-qty-btn" onclick="setPdfDpi(1200)">1200 DPI</button>
            <input type="number" id="manualDpiInput" class="qty-input" value="300" min="50" max="1200" oninput="updateManualDpi(this.value)">
          </div>
          <div style="margin-top: 10px; font-size: 13px;">
            Current Active DPI: <strong id="currentDpiDisplay" style="color:#fbbf24;">300 DPI</strong>
          </div>
        </div>

        <div style="margin-top: 10px; font-size: 12px; color: var(--text-muted);" id="pdfConversionProgress"></div>

        <div class="btn-group">
          <button id="startPdfToJpgBtn" class="action-btn btn-download">🖼️ Convert & Download JPGs</button>
        </div>
      </div>
    </div>

    <!-- TAB 9: PDF COMPRESSOR -->
    <div id="tab-pdf-compressor" class="tab-content">
      <div class="badge">Interactive Quality & Size Slider • Target KB/MB Preview • High-Speed Export</div>
      <h1>PDF Size Compressor</h1>
      <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 12px;">PDF फ़ाइल अपलोड करें, स्लाइडर से अपनी मनचाही फाइल साइज़ (KB/MB) सेट करें और डाउनलोड करें।</p>

      <div class="upload-section" style="margin-bottom: 15px;">
        <label class="upload-box" for="pdfCompressInput" style="max-width: 420px;">
          <strong style="display:block; font-size:14px; margin-bottom:4px; color:var(--accent-blue);">🗜️ Select PDF to Compress</strong>
          <div id="pdfCompressStatus" style="font-size: 12px; color: var(--text-muted);">क्लिक करके .pdf फाइल चुनें</div>
        </label>
        <input type="file" id="pdfCompressInput" accept="application/pdf">
      </div>

      <div id="compressorControlsArea" style="display:none;">
        <div class="control-panel">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size: 13px; font-weight:600; color: var(--accent-blue);">🎚️ Compression Quality Slider:</span>
            <span id="compressQualityLabel" style="font-weight:700; color:#fbbf24;">60% (Medium)</span>
          </div>

          <input type="range" id="compressQualitySlider" class="slider-range" min="10" max="95" value="60" oninput="onCompressSliderChange(this.value)">

          <div class="size-badge-box">
            <div>
              <div style="font-size:11px; color:var(--text-muted);">Original File Size</div>
              <strong id="origFileSizeDisplay" style="color:#f87171; font-size:14px;">0 KB</strong>
            </div>
            <div>
              <div style="font-size:11px; color:var(--text-muted);">Estimated Download Size</div>
              <strong id="estFileSizeDisplay" style="color:#34d399; font-size:14px;">0 KB</strong>
            </div>
          </div>
        </div>

        <div style="margin-top: 10px; font-size: 12px; color: var(--text-muted);" id="compressProgressMsg"></div>

        <div class="btn-group">
          <button id="startCompressDownloadBtn" class="action-btn btn-download">📥 Compress & Download PDF</button>
        </div>
      </div>
    </div>

    <!-- TAB 10: HISTORY (WITH WORKING DOWNLOAD & ALERT WARNING) -->
    <div id="tab-history" class="tab-content">
      <div class="badge">Persistent Storage • Download Ready</div>
      <h1>Print & Download History</h1>
      <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 12px;">आपके द्वारा डाउनलोड की गई सभी फाइल्स का रिकॉर्ड सुरक्षित है। आप यहाँ से डाउनलोड भी कर सकते हैं और डिलीट भी कर सकते हैं।</p>

      <!-- Warning Alert Box for Browser History Clear -->
      <div style="background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.5); color: #fde68a; padding: 10px 14px; border-radius: 8px; margin-bottom: 12px; font-size: 12px; text-align: left; display: flex; align-items: center; gap: 8px;">
        <span style="font-size: 16px;">⚠️</span>
        <span><strong>महत्वपूर्ण चेतावनी:</strong> यदि आप अपने ब्राउज़र का डेटा (Browser Data/History) क्लियर करते हैं, तो यह डाउनलोड हिस्ट्री हमेशा के लिए डिलीट हो जाएगी। कृपया समय पर इसका बैकअप रखें।</span>
      </div>

      <div style="text-align: right; margin-bottom: 10px;">
        <button onclick="clearAllHistoryDB()" class="action-btn btn-reset" style="padding: 6px 14px; font-size: 11px;">🗑️ Clear Entire History Now</button>
      </div>

      <div class="history-table-container">
        <table class="history-table">
          <thead>
            <tr>
              <th>Type / Feature</th>
              <th>File Name</th>
              <th>Generated Time</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody id="historyTableBody">
            <tr>
              <td colspan="4" style="text-align:center; color:var(--text-muted); padding:20px;">कोई प्रिंट रिकॉर्ड नहीं मिला।</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- TAB 11: ADMIN PANEL -->
    <div id="tab-admin" class="tab-content">
      <div class="badge" style="background: rgba(245, 158, 11, 0.15); color: #fbbf24; border-color: rgba(245, 158, 11, 0.4);">Master Administrator Panel <button id="lockAdminPanelBtn" type="button" class="login-btn">🔒 Lock Panel</button></div>
      <h1 style="color: #fbbf24;">Cloud Distributor Management</h1>
      <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 20px;">नए डिस्ट्रीब्यूटर जोड़ें। डिस्ट्रीब्यूटर की वैलिडिटी 30 दिनों की होगी और डेटा सुरक्षित रहेगा।</p>

      <div class="control-panel" style="max-width: 500px; text-align: left; margin-bottom: 25px;">
        <h3 style="font-size: 14px; color: var(--accent-blue); margin-bottom: 12px;">➕ Add New Distributor</h3>
        <div style="display:flex; flex-direction:column; gap:10px;">
          <div>
            <label style="font-size: 11px; color: var(--text-muted); display:block; margin-bottom:4px;">Business / Name:</label>
            <input type="text" id="newDistName" class="text-field-input" style="max-width:100%;" placeholder="e.g. Shri Ganesh Digital Seva">
          </div>
          <div>
            <label style="font-size: 11px; color: var(--text-muted); display:block; margin-bottom:4px;">Distributor Email (Login ID):</label>
            <input type="email" id="newDistEmail" class="text-field-input" style="max-width:100%;" placeholder="user@gmail.com">
          </div>
          <div>
            <label style="font-size: 11px; color: var(--text-muted); display:block; margin-bottom:4px;">Assign Password:</label>
            <input type="text" id="newDistPass" class="text-field-input" style="max-width:100%;" placeholder="SecurePass123">
          </div>
          <button onclick="addNewDistributor()" class="action-btn btn-add" style="margin-top: 5px;">🚀 Assign ID & Password</button>
          <div id="distMsg" style="font-size: 12px; font-weight: 500; display:none; margin-top:5px;"></div>
        </div>
      </div>

      <h3 style="font-size: 14px; color: var(--accent-blue); margin-bottom: 10px; text-align: left; max-width: 850px; margin-left: auto; margin-right: auto;">Connected Distributors List (30 Days Validity)</h3>
      <div class="history-table-container" style="max-width: 850px; margin-left: auto; margin-right: auto;">
        <table class="history-table">
          <thead>
            <tr>
              <th>Business / Name</th>
              <th>Login Email</th>
              <th>Account Security</th>
              <th>Payment / Screenshot Link</th>
              <th>Validity / Timeline</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody id="distributorTableBody">
            <tr>
              <td colspan="6" style="text-align:center; color:var(--text-muted); padding:15px;">डेटा लोड हो रहा है...</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <footer style="margin-top: 25px; font-size: 12px; color: var(--text-muted);">
      Designed & Developed by <strong>JAYESH BHAVSAR @ 2026 ALL RIGHTS RESERVED</strong>
    </footer>
  </div>
</div>

<!-- Global Crop Modal -->
<div id="cropModal">
  <div id="cropModalTitle" style="color:#fff; margin-bottom: 10px; font-weight: 600;">कार्ड/फ़ोटो का सही हिस्सा सेलेक्ट (Crop) करें:</div>
  <div class="crop-wrapper">
    <img id="imageToCrop" src="">
  </div>
  <div class="btn-group">
    <button id="cropSaveBtn" class="action-btn btn-download">✂️ Crop & Set</button>
    <button id="cropCancelBtn" class="action-btn" style="background:#ef4444;">रद्द करें</button>
  </div>
</div>

<!-- Admin Message & Image Modal -->
<div id="adminMsgModal">
  <div class="auth-box" style="max-width:440px; text-align:left;">
    <h3 style="color: var(--accent-blue); margin-bottom: 10px; font-size: 18px;">💬 Send Notice & QR Code to Distributor</h3>
    <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 15px;">यह मैसेज और QR कोड केवल इस विशेष डिस्ट्रीब्यूटर को दिखेगा।</p>
    <input type="hidden" id="targetDistEmail">
    
    <label style="font-size: 11px; color: var(--text-muted); display: block; margin-bottom: 4px;">✍️ Message / Notice:</label>
    <textarea id="adminTypedMsg" class="login-input" style="height: 75px; resize:none;" placeholder="यहाँ अपना मैसेज टाइप करें..."></textarea>
    
    <label style="font-size: 12px; color: #38bdf8; display: block; margin-bottom: 6px; font-weight: 600;">🖼️ Attach QR Code / Banner Image (Optional):</label>
    <div style="background: rgba(15,23,42,0.9); border: 1px dashed var(--accent-blue); padding: 12px; border-radius: 8px; margin-bottom: 15px; text-align: center;">
      <input type="file" id="adminNoticeImgInput" accept="image/*" style="display: block; width: 100%; color: #fff; font-size: 12px; cursor: pointer;">
    </div>
    
    <div style="display: flex; gap: 10px;">
      <button onclick="saveAdminMessage()" class="action-btn btn-download" style="flex:1;">📤 Send Message & QR</button>
      <button onclick="closeAdminMsgModal()" class="action-btn btn-reset" style="flex:1;">रद्द करें</button>
    </div>
  </div>
</div>

<!-- View Distributor Screenshot Modal for Admin -->
<div id="viewScreenshotModal">
  <div class="auth-box" style="max-width:450px; text-align:center;">
    <h3 style="color: var(--accent-blue); margin-bottom: 10px; font-size: 18px;">📸 Distributor Payment Screenshot</h3>
    <p style="font-size: 11px; color: var(--text-muted); margin-bottom: 12px;">डिस्ट्रीब्यूटर द्वारा भेजा गया भुगतान का स्क्रीनशॉट:</p>
    <div style="background:#000; padding:10px; border-radius:8px; margin-bottom:15px; border:1px solid var(--border-color);">
      <img id="adminViewScreenshotImg" src="" style="max-width:100%; max-height:350px; border-radius:6px; display:block; margin:0 auto;" alt="Screenshot">
    </div>
    <button onclick="closeViewScreenshotModal()" class="action-btn btn-reset" style="width:100%;">❌ बंद करें (Close)</button>
  </div>
</div>

<!-- Contact for Registration Popup Modal -->
<div id="regModalPopup">
  <div class="reg-popup-content">
    <h3 style="color: var(--accent-blue); margin-bottom: 10px; font-size: 18px;">📞 Contact for Registration</h3>
    <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 20px;">पोर्टल रजिस्ट्रेशन और पूछताछ के लिए संपर्क करें:</p>
    
    <div style="background: rgba(15,23,42,0.8); padding: 12px; border-radius: 10px; margin-bottom: 12px; border: 1px solid var(--border-color); text-align: left;">
      <div style="font-size: 11px; color: var(--text-muted);">📱 WhatsApp Helpline:</div>
      <a href="https://wa.me/917887575671?text=Hello%20Sir,%20I%20want%20to%20register%20for%20ID%20Printing%20Portal." target="_blank" style="color: #34d399; font-weight: 700; font-size: 14px; text-decoration: none;">+91 7887575671</a>
    </div>

    <div style="background: rgba(15,23,42,0.8); padding: 12px; border-radius: 10px; margin-bottom: 20px; border: 1px solid var(--border-color); text-align: left;">
      <div style="font-size: 11px; color: var(--text-muted);">📧 Official Email IDs:</div>
      <a href="mailto:idprintingportal@gmail.com" style="color: #38bdf8; font-weight: 600; font-size: 13px; text-decoration: none;">idprintingportal@gmail.com</a><br>
      <a href="mailto:oneplus777000@gmail.com" style="color: #38bdf8; font-weight: 600; font-size: 13px; text-decoration: none;">oneplus777000@gmail.com</a>
    </div>

    <button onclick="closeRegModal()" class="action-btn" style="background: #ef4444; width: 100%;">❌ बंद करें (Close)</button>
  </div>
</div>

<script>
  // ==========================================================
  // REGISTRATION MODAL POPUP FUNCTIONS
  // ==========================================================
  function openRegModal() {
    document.getElementById('regModalPopup').style.display = 'flex';
  }
  function closeRegModal() {
    document.getElementById('regModalPopup').style.display = 'none';
  }

  // ==========================================================
  // CLOUD API URL (POST JSON Method)
  // ==========================================================
  const GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxhAJ-GhVFqlNsimIap4r_eZD68LPi_EGf1yMPS82aOpMHP-oDGmJ64D73oXiLRsoaP/exec";

  let authToken = '';
  let authRole = '';
  let authEmail = '';
  let authExpires = 0;
  let adminPanelUntil = 0;
  let adminUnlockPending = null;
  let adminLockRequest = Promise.resolve();
  let distributorMemoryCache = [];
  try { localStorage.removeItem('distributorLocalCache'); localStorage.removeItem('system_auth_pwd'); } catch (_) {}

  function getDistributorCache() { return distributorMemoryCache; }
  function saveDistributorCache(list) { distributorMemoryCache = Array.isArray(list) ? list : []; }
  function mergeDistributorCache(list) { saveDistributorCache(list); return distributorMemoryCache; }
  function acceptSession(result, email) {
    authToken=result.token; authRole=result.role; authEmail=email; authExpires=result.expires;
    distributorMemoryCache=[];
  }
  function clearAuth() {
    window.dispatchEvent(new Event('portal-auth-cleared'));
    adminPanelUntil=0;
    if(adminUnlockPending) finishAdminUnlock(false);
    authToken=''; authRole=''; authEmail=''; authExpires=0; distributorMemoryCache=[];
    activeDistributorSession=null; currentRenewalDistributor=null; currentLoggedDistributorEmail='';
    sessionStorage.removeItem('isLoggedIn');
    document.getElementById('distributorTableBody').replaceChildren();
    document.getElementById('historyTableBody').replaceChildren();
  }
  async function secureApi(payload) {
    const requestToken=authToken;
    const response=await fetch(GOOGLE_SCRIPT_URL, {method:'POST', cache:'no-store', credentials:'omit',
      headers:{'Content-Type':'text/plain;charset=UTF-8'}, body:JSON.stringify({...payload, token:requestToken})});
    if(!response.ok) throw new Error('Server unavailable. Please retry.');
    const result=await response.json();
    if(!['login','register'].includes(payload.action) && requestToken!==authToken) throw new Error('Account changed. Please retry.');
    if(!result || result.success!==true) throw new Error(result?.error || 'Server did not confirm the action.');
    return result;
  }
  async function getDistributorsListCloud() {
    if(!authToken) return [];
    const result=await secureApi({action:authRole==='admin'?'getDistributors':'getMe'});
    const list=authRole==='admin'?result.records:(result.record?[result.record]:[]);
    saveDistributorCache(list); return list;
  }
  async function callRenewalPost(payload) { return secureApi(payload); }
  async function callCloudPost(payload) {
    try { return await secureApi(payload); }
    catch(error) { alert(error.message); return false; }
  }
  async function callCloudGet(params) { return callCloudPost(Object.fromEntries(params.entries())); }
  async function addDistributorCloud(record) {
    const result=await callCloudPost({...record,action:authRole==='admin'?'addDistributor':'register'});
    if(result?.token) acceptSession(result,record.email);
    return result;
  }
  async function uploadScreenshotCloud(email,imageData,fileName) {
    try { return await secureApi({action:'uploadPaymentScreenshot',email,imageData,fileName}); }
    catch(error) { return {success:false,error:error.message}; }
  }
  function escapeHtml(value) {
    return String(value ?? '').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  }
  function safeImageUrl(value) {
    try {
      const url=new URL(String(value || ''));
      // Existing Drive screenshots and current ImgBB uploads are the only supported external images.
      return url.protocol==='https:' && !url.username && !url.password && ['i.ibb.co','ibb.co','drive.google.com','lh3.googleusercontent.com'].includes(url.hostname) ? url.href : '';
    } catch(_) { return ''; }
  }
  function openDistributorScreenshot(value) {
    const url=safeImageUrl(value);
    if(!url) return alert('Screenshot URL is invalid or unsupported.');
    window.open(url,'_blank','noopener,noreferrer');
  }
  async function renderDistributorsTable() {
    if(authRole!=='admin' || Date.now()>=adminPanelUntil) return;
    const tbody=document.getElementById('distributorTableBody');
    tbody.textContent='Loading…';
    let records;
    try { records=await getDistributorsListCloud(); }
    catch(error) { tbody.textContent=error.message; return; }
    if(authRole!=='admin' || Date.now()>=adminPanelUntil) {tbody.replaceChildren();return;}
    tbody.replaceChildren();
    for(const d of records) {
      const tr=document.createElement('tr');
      const cell=text=>{const td=document.createElement('td');td.textContent=String(text ?? '');tr.appendChild(td);return td;};
      cell(d.name);cell(d.email);cell('Password protected');
      const renewal=String(d.renewalRequested).toLowerCase()==='true';
      const payment=cell(`${d.paymentStatus || ''}\n${renewal?'🔄 Renewal Request\n':''}${renewal?d.renewalPlan:d.paymentPlan} | ${renewal?d.renewalAmount:d.paymentAmount}\nTxn: ${renewal?d.renewalTxnId:d.paymentTxnId}`);
      payment.style.whiteSpace='pre-line';
      const days=Math.max(0,Math.ceil((Number(d.expiryTime)-Date.now())/86400000));
      cell(`${days} Days Left | ${d.status}`);
      const actions=cell('');
      const button=(label,fn)=>{const b=document.createElement('button');b.type='button';b.className='history-msg-btn';b.textContent=label;b.style.margin='3px';b.addEventListener('click',async()=>{b.disabled=true;try{await fn();}catch(error){alert(error.message);}finally{b.disabled=false;}});actions.appendChild(b);};
      const image=safeImageUrl(renewal?d.renewalScreenshot:d.paymentScreenshot);
      if(image) button('🔗 Open Screenshot',()=>openDistributorScreenshot(image));
      if(d.distributorMessage) {const text=document.createElement('div');text.textContent=d.distributorMessage;actions.appendChild(text);}
      const reply=safeImageUrl(d.distributorReplyImage);
      if(reply) button('🔗 Open Reply Image',()=>openDistributorScreenshot(reply));
      button('💬 Message',()=>openAdminMsgModal(d.email));
      if(String(d.paymentStatus).toLowerCase()==='pending') {
        button('✅ Approve',()=>reviewDistributorPayment(d.email,true));
        button('❌ Reject',()=>reviewDistributorPayment(d.email,false));
      }
      button('🛑 Stop',()=>toggleDistributorStatus(d.email,'Stopped'));
      button('▶️ Start',()=>toggleDistributorStatus(d.email,'Active'));
      button('🗑️ Delete',()=>removeDistributor(d.id));
      tbody.appendChild(tr);
    }
  }
  function finishAdminUnlock(success) {
    const pending=adminUnlockPending;adminUnlockPending=null;
    document.getElementById('adminUnlockModal').style.display='none';
    document.getElementById('adminUnlockPassword').value='';
    if(pending) pending.resolve(success);
  }
  function requestAdminUnlock() {
    if(authRole!=='admin') return Promise.resolve(false);
    if(adminUnlockPending) return adminUnlockPending.promise;
    const modal=document.getElementById('adminUnlockModal');
    document.getElementById('adminUnlockError').textContent='';
    document.getElementById('adminUnlockPassword').value='';
    document.getElementById('adminUnlockSubmit').disabled=false;
    const promise=new Promise(resolve=>{adminUnlockPending={resolve};});
    adminUnlockPending.promise=promise;
    modal.style.display='flex';document.getElementById('adminUnlockPassword').focus();
    return promise;
  }
  async function submitAdminUnlock(event) {
    event.preventDefault();
    const pending=adminUnlockPending;
    if(!pending) return;
    const button=document.getElementById('adminUnlockSubmit');
    if(button.disabled) return;
    button.disabled=true;
    button.textContent='Verifying…';
    try {
      await adminLockRequest;
      const result=await secureApi({action:'unlockAdminPanel',password:document.getElementById('adminUnlockPassword').value});
      if(adminUnlockPending!==pending) {lockAdminPanel();return;}
      adminPanelUntil=result.panelUntil;finishAdminUnlock(true);
    } catch(error) {
      if(adminUnlockPending===pending) document.getElementById('adminUnlockError').textContent=error.message;
    } finally {
      document.getElementById('adminUnlockPassword').value='';button.disabled=false;button.textContent='Unlock Panel';
    }
  }
  function lockAdminPanel() {
    adminPanelUntil=0;
    distributorMemoryCache=[];
    if(adminUnlockPending) finishAdminUnlock(false);
    document.getElementById('distributorTableBody').replaceChildren();
    document.getElementById('adminMsgModal').style.display='none';
    document.getElementById('viewScreenshotModal').style.display='none';
    if(authRole==='admin' && authToken) adminLockRequest=secureApi({action:'lockAdminPanel'}).catch(()=>{});
    if(document.getElementById('tab-admin').classList.contains('active')) showPortalTab('tab-cards');
  }
  function showPortalTab(tabId) {
    document.querySelectorAll('.tab-btn').forEach(btn=>btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content=>content.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
    document.querySelectorAll('.tab-btn').forEach(btn=>{if((btn.getAttribute('onclick')||'').includes("'"+tabId+"'"))btn.classList.add('active');});
  }
  async function switchTab(tabId) {
    if(!authToken || (tabId==='tab-admin' && authRole!=='admin')) return;
    if(tabId==='tab-admin') {
      if(Date.now()>=adminPanelUntil && !(await requestAdminUnlock())) return;
      if(authRole!=='admin' || Date.now()>=adminPanelUntil) return;
      showPortalTab(tabId);await renderDistributorsTable();return;
    }
    if(adminPanelUntil || adminUnlockPending) lockAdminPanel();
    showPortalTab(tabId);
    if(tabId==='tab-history') renderHistoryTable();
  }
  function switchTabDirect(tabId) {
    if (!authToken || (tabId === 'tab-admin' && authRole !== 'admin')) return;
    if(!authToken || (tabId==='tab-admin' && (authRole!=='admin'||Date.now()>=adminPanelUntil))) return;
    if(tabId!=='tab-admin' && adminPanelUntil) lockAdminPanel();
    showPortalTab(tabId);
  }
  async function reviewDistributorPayment(email,approved) {
    if(!confirm(approved?'Approve this payment?':'Reject this payment?')) return;
    await secureApi({action:'reviewDistributorPayment',email,approved:String(approved)});
    await renderDistributorsTable();
    alert(approved?'✅ Approved. Validity saved by the server.':'✅ Rejected. Access remains closed.');
  }
  function showPendingScreen(record,state) {
    activeDistributorSession=null;
    mainApp.style.display='none';loginScreen.style.display='none';renewalScreen.style.display='none';signUpScreen.style.display='none';changePwdScreen.style.display='none';
    document.getElementById('pendingScreen').style.display='block';
    document.getElementById('pendingStatus').textContent=state==='rejected'?'Payment rejected. Contact admin or upload corrected proof.':'Your application is awaiting admin approval.';
  }
  async function handleLogin() {
    const email=loginEmail.value.trim().toLowerCase(), password=loginPass.value;
    authBtn.disabled=true;
    try {
      const previousToken=authToken;
      if(previousToken) { try {await secureApi({action:'logout'});} catch(_) {} }
      clearAuth();
      const result=await secureApi({action:'login',email,password});
      acceptSession(result,email);
      loginPass.value=''; errorMsg.style.display='none';
      document.getElementById('pendingScreen').style.display='none';
      if(result.role==='distributor') {
        if(result.state==='renewal'||result.state==='renewal_pending') {showRenewalScreen(result.record);return;}
        if(result.state==='pending'||result.state==='rejected') {showPendingScreen(result.record,result.state);return;}
        if(result.state!=='active') throw new Error('Your account is stopped. Please contact admin.');
      }
      activeDistributorSession=result.record;
      loginScreen.style.display='none';changePwdScreen.style.display='none';renewalScreen.style.display='none';mainApp.style.display='block';
      document.getElementById('topNavRegistrationBox').style.display='none';
      adminTabBtn.style.display=result.role==='admin'?'inline-block':'none';
      if(result.role==='admin') {updateValidityDisplay();switchTabDirect('tab-cards');}
      else {
        currentLoggedDistributorEmail=email;renderDistributorNotice(result.record);switchTabDirect('tab-cards');
        const days=Math.max(0,Math.ceil((Number(result.record.expiryTime)-Date.now())/86400000));
        document.getElementById('validityCounterBadge').textContent=`👤 ${result.record.name} | Validity: ${days} Days Left`;
      }
      initAllCanvases();
    } catch(error) {
      clearAuth();mainApp.style.display='none';loginScreen.style.display='block';
      errorMsg.textContent=error.message;errorMsg.style.display='block';
    } finally {authBtn.disabled=false;}
  }
  async function changePasswordFromForm() {
    const newPass=newPassInput.value;
    pwdStatusMsg.style.display='block';
    if(newPass!==confirmPassInput.value) {pwdStatusMsg.textContent='Passwords do not match.';return;}
    saveNewPwdBtn.disabled=true;
    try {
      await secureApi({action:'updatePassword',email:pwdEmailInput.value.trim().toLowerCase(),oldPass:oldPassInput.value,newPass});
      clearAuth();oldPassInput.value='';newPassInput.value='';confirmPassInput.value='';
      pwdStatusMsg.textContent='Password updated. All old sessions are invalid. Please login again.';
      setTimeout(()=>location.reload(),2000);
    } catch(error) {pwdStatusMsg.textContent=error.message;}
    finally {saveNewPwdBtn.disabled=false;}
  }
  let checkingSession=false;
  async function checkServerSession() {
    if(!authToken || checkingSession) return;
    checkingSession=true;
    try {
      if(Date.now()>=authExpires) throw new Error('Session expired. Please login again.');
      const result=await secureApi({action:'getMe'});
      if(result.role==='distributor') {
        if(result.state==='renewal'||result.state==='renewal_pending') {
          if(mainApp.style.display!=='none') showRenewalScreen(result.record);
        } else if(result.state==='pending'||result.state==='rejected') showPendingScreen(result.record,result.state);
        else if(result.state!=='active') throw new Error('Account stopped. Contact admin.');
        else {activeDistributorSession=result.record;renderDistributorNotice(result.record);}
      }
    } catch(error) {
      clearAuth();mainApp.style.display='none';renewalScreen.style.display='none';document.getElementById('pendingScreen').style.display='none';loginScreen.style.display='block';
      errorMsg.textContent=error.message;errorMsg.style.display='block';
    } finally {checkingSession=false;}
  }








  function getDistributorScreenshotUrl(record) {
    if (!record || typeof record !== 'object') return '';
    const candidates = [
      record.renewalScreenshot,
      record.paymentScreenshot,
      record.distScreenshot,
      record.distscreenshot,
      record.dist_screenshot,
      record.screenshot,
      record.districtsx,
      record.paymentProof,
      record.proofScreenshot
    ];

    for (const value of candidates) {
      if (typeof value === 'string' && value.trim() !== '') return value.trim();
    }
    return '';
  }

  function isDistributorAccessApproved(record) {
    if (!record || typeof record !== 'object') return false;

    const paymentStatus = String(record.paymentStatus || record.approvalStatus || '').trim().toLowerCase();
    const distStatus = String(record.status || '').trim().toLowerCase();
    const approvalGranted = [record.approvalGranted, record.approved, record.accessApproved].some(value => String(value).toLowerCase() === 'true');

    return approvalGranted && paymentStatus === 'approved' && distStatus === 'active';
  }







  async function refreshDistributorCloudData() {
    try {
      const latest = await getDistributorsListCloud();
      if (Array.isArray(latest)) {
        saveDistributorCache(latest);
      }
      return latest;
    } catch (err) {
      console.error('Distributor refresh failed:', err);
      return [];
    }
  }





  async function deleteDistributorCloud(distId) {
    return await callCloudGet(new URLSearchParams({ action: 'deleteDistributor', id: distId }));
  }

  async function sendAdminMsgCloud(email, message, imageUrl) {
    return await callCloudPost({ action: "messageDistributor", email, message, imageUrl });
  }



  async function toggleDistributorStatusCloud(email, newStatus) {
    const normalizedStatus = String(newStatus || 'Active').trim();
    return await callCloudGet(new URLSearchParams({
      action: 'toggleStatus',
      email,
      status: normalizedStatus
    }));
  }

  async function updateDistributorPasswordCloud(email, newPass) {
    return await callCloudPost({ action: "updatePassword", email: email, newPass: newPass });
  }

  // ==========================================================
  // INDEXEDDB HISTORY STORAGE ENGINE
  // ==========================================================
  const DB_NAME = 'PrintPortalPrivateHistory-v4:';
  const DB_STORE = 'print_records';

  function openHistoryDB() {
    if (!authToken || !authEmail) return Promise.reject(new Error('Login required.'));
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(DB_NAME + authEmail, 1);
      request.onupgradeneeded = function(e) {
        const db = e.target.result;
        if (!db.objectStoreNames.contains(DB_STORE)) {
          db.createObjectStore(DB_STORE, { keyPath: 'id', autoIncrement: true });
        }
      };
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  async function saveToHistory(featureName, fileName, blobOrDataUrl, fileType) {
    try {
      const db = await openHistoryDB();
      const tx = db.transaction(DB_STORE, 'readwrite');
      const store = tx.objectStore(DB_STORE);
      
      const record = {
        feature: featureName,
        fileName: fileName,
        data: blobOrDataUrl,
        fileType: fileType,
        timestamp: Date.now(),
        dateFormatted: new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' })
      };

      store.add(record);
    } catch(err) {}
  }

  async function renderHistoryTable() {
    try {
      const db = await openHistoryDB();
      const tx = db.transaction(DB_STORE, 'readonly');
      const store = tx.objectStore(DB_STORE);
      const request = store.getAll();

      request.onsuccess = function() {
        const records = request.result || [];
        const tbody = document.getElementById('historyTableBody');
        tbody.innerHTML = '';

        if (!records.length) {
          tbody.innerHTML = `<tr><td colspan="4" style="text-align:center; color:var(--text-muted); padding:20px;">कोई प्रिंट रिकॉर्ड नहीं मिला।</td></tr>`;
          return;
        }

        records.reverse().forEach(rec => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td><strong style="color:var(--accent-blue);">${escapeHtml(rec.feature)}</strong></td>
            <td>${escapeHtml(rec.fileName)}</td>
            <td style="color:#94a3b8; font-size:11px;">${escapeHtml(rec.dateFormatted)}</td>
            <td>
              <button class="history-download-btn" onclick="reDownloadHistoryFile(${Number(rec.id)})">📥 Download</button>
              <button class="history-delete-btn" onclick="deleteHistoryRecord(${Number(rec.id)})" style="margin-left: 5px;">🗑️ Delete</button>
            </td>
          `;
          tbody.appendChild(tr);
        });
      };
    } catch(err) {}
  }

  async function reDownloadHistoryFile(recordId) {
    const db = await openHistoryDB();
    const tx = db.transaction(DB_STORE, 'readonly');
    const store = tx.objectStore(DB_STORE);
    const request = store.get(recordId);

    request.onsuccess = function() {
      const rec = request.result;
      if (!rec) return;

      const link = document.createElement('a');
      if (typeof rec.data === 'string') {
        link.href = rec.data;
      } else {
        link.href = URL.createObjectURL(rec.data);
      }
      link.download = rec.fileName;
      link.click();
    };
  }

  async function deleteHistoryRecord(recordId) {
    if (!confirm('क्या आप इस रिकॉर्ड को हटाना चाहते हैं?')) return;
    const db = await openHistoryDB();
    const tx = db.transaction(DB_STORE, 'readwrite');
    const store = tx.objectStore(DB_STORE);
    store.delete(recordId);
    tx.oncomplete = () => renderHistoryTable();
  }

  async function clearAllHistoryDB() {
    if (!confirm('क्या आप सभी इतिहास रिकॉर्ड्स हमेशा के लिए मिटाना चाहते हैं?')) return;
    const db = await openHistoryDB();
    const tx = db.transaction(DB_STORE, 'readwrite');
    tx.objectStore(DB_STORE).clear();
    tx.oncomplete = () => renderHistoryTable();
  }

  if (typeof pdfjsLib !== 'undefined') {
    pdfjsLib.GlobalWorkerOptions.workerSrc = '';
  }

  const ADMIN_EMAIL = "oneplus777000@gmail.com";
  const THIRTY_DAYS = 30;
  const THIRTY_MS = THIRTY_DAYS * 24 * 60 * 60 * 1000;
  const ONE_YEAR_DAYS = 365;
  const ONE_YEAR_MS = ONE_YEAR_DAYS * 24 * 60 * 60 * 1000;
  const PAYMENT_PLAN_OPTIONS = {
    '1month': { label: '1 Month', amount: 36, ms: THIRTY_MS },
    '1year': { label: '1 Year', amount: 319, ms: ONE_YEAR_MS }
  };



  function updateValidityDisplay() {
    const badge = document.getElementById('validityCounterBadge');
    badge.innerHTML = `⏳ Admin Account: <strong style="color:#34d399;">Lifetime Access (No Expiry)</strong>`;
    badge.style.borderColor = '#10b981';
    badge.style.color = '#34d399';
    badge.style.background = 'rgba(16, 185, 129, 0.15)';
  }

  // ==========================================================
  // DISTRIBUTOR MANAGEMENT
  // ==========================================================
  async function addNewDistributor() {
    const name = document.getElementById('newDistName').value.trim();
    const email = document.getElementById('newDistEmail').value.trim().toLowerCase();
    const pass = document.getElementById('newDistPass').value;
    const msg = document.getElementById('distMsg');

    if (!name || !email || !pass) {
      msg.innerText = "⚠️ कृपया सभी फ़ील्ड भरें!";
      msg.style.color = "#ef4444";
      msg.style.display = "block";
      return;
    }

    if (email === ADMIN_EMAIL.toLowerCase()) {
      msg.innerText = "⚠️ यह ईमेल एडमिन ईमेल है!";
      msg.style.color = "#ef4444";
      msg.style.display = "block";
      return;
    }

    let currentList = await getDistributorsListCloud();
    if (currentList.some(d => String(d.email).toLowerCase() === email)) {
      msg.innerText = "⚠️ यह ईमेल आईडी पहले से मौजूद है!";
      msg.style.color = "#ef4444";
      msg.style.display = "block";
      return;
    }

    const assignedTimestamp = Date.now();
    const distExpiryTime = assignedTimestamp + THIRTY_MS;

    const newDistData = {
      id: Date.now(),
      name: name,
      email: email,
      pass: pass,
      assignedTimestamp: assignedTimestamp,
      expiryTime: distExpiryTime,
      adminMessage: "",
      status: "Active",
      paymentStatus: "Approved",
      paymentTxnId: "Admin Assignment",
      approvalNote: "Admin created account manually"
    };

    let success = await addDistributorCloud(newDistData);
    if (success) {
      msg.innerText = "✅ डिस्ट्रीब्यूटर सफलतापूर्वक जोड़ दिया गया है!";
      msg.style.color = "#34d399";
      msg.style.display = "block";

      document.getElementById('newDistName').value = '';
      document.getElementById('newDistEmail').value = '';
      document.getElementById('newDistPass').value = '';

      setTimeout(() => renderDistributorsTable(), 1500);
    } else {
      msg.innerText = "⚠️ जोड़ने में समस्या आई, पुनः प्रयास करें!";
      msg.style.color = "#ef4444";
      msg.style.display = "block";
    }
  }



  function viewDistributorScreenshot(ssUrl) {
    document.getElementById('adminViewScreenshotImg').src = safeImageUrl(decodeURIComponent(ssUrl));
    document.getElementById('viewScreenshotModal').style.display = 'flex';
  }



  function closeViewScreenshotModal() {
    document.getElementById('viewScreenshotModal').style.display = 'none';
  }



  async function toggleDistributorStatus(email, newStatus) {
    if (!confirm(`क्या आप इस डिस्ट्रीब्यूटर की सर्विस को ${newStatus === 'Stopped' ? '🛑 Stop (रोकना)' : '▶️ Start (चालू करना)'} चाहते हैं?`)) return;

    const result = await toggleDistributorStatusCloud(email, newStatus);
    if (result) {
      await refreshDistributorCloudData();
      renderDistributorsTable();
    }
  }

  async function removeDistributor(id) {
    if (!confirm('क्या आप इस डिस्ट्रीब्यूटर को हटाना चाहते हैं?')) return;
    const result = await deleteDistributorCloud(id);
    if (result) {
      await refreshDistributorCloudData();
      renderDistributorsTable();
    }
  }

  function openAdminMsgModal(email) {
    document.getElementById('targetDistEmail').value = email;
    document.getElementById('adminTypedMsg').value = '';
    document.getElementById('adminNoticeImgInput').value = '';
    document.getElementById('adminMsgModal').style.display = 'flex';
  }

  function closeAdminMsgModal() {
    document.getElementById('adminMsgModal').style.display = 'none';
  }

  async function saveAdminMessage() {
    const email = document.getElementById('targetDistEmail').value;
    const msgText = document.getElementById('adminTypedMsg').value.trim();
    const imgFile = document.getElementById('adminNoticeImgInput').files[0];

    if (!msgText && !imgFile) {
      alert('कृपया कुछ मैसेज या इमेज अटैच करें!');
      return;
    }

    let imageUrl = "";
    if (imgFile) {
      imageUrl = await preparePaymentScreenshot(imgFile);
    }

    const result = await sendAdminMsgCloud(email, msgText, imageUrl);
    if (!result) {
      alert('⚠️ मैसेज भेजने में समस्या हुई। कृपया पुनः प्रयास करें।');
      return;
    }

    alert('✅ मैसेज और QR कोड सफलतापूर्वक भेज दिया गया है!');
    closeAdminMsgModal();
    await refreshDistributorCloudData();
    renderDistributorsTable();
  }

  // Active Logged-in Distributor Email storage
  let currentLoggedDistributorEmail = "";

  function renderDistributorNotice(record) {
    const banner = document.getElementById('distributorNoticeBanner');
    const txtSpan = document.getElementById('distributorNoticeText');
    const imgBox = document.getElementById('distributorNoticeImgBox');
    const imgElem = document.getElementById('distributorNoticeImg');
    if (!banner || !txtSpan || !imgBox || !imgElem) return;

    const noticeText = record?.adminmessage || record?.adminMessage || '';
    const noticeImg = record?.adminimage || record?.adminImage || '';
    const hasText = String(noticeText).trim() !== '';
    const hasImage = Boolean(safeImageUrl(noticeImg));

    txtSpan.innerText = hasText ? noticeText : '';
    if (hasImage) {
      imgElem.src = safeImageUrl(noticeImg);
      imgBox.style.display = 'block';
    } else {
      imgElem.removeAttribute('src');
      imgBox.style.display = 'none';
    }

    banner.style.display = hasText || hasImage ? 'block' : 'none';
  }

  async function refreshDistributorNotice() {
    if (!currentLoggedDistributorEmail) return;
    const dists = await getDistributorsListCloud();
    const record = dists.find((dist) => String(dist.email || '').trim().toLowerCase() === currentLoggedDistributorEmail);
    renderDistributorNotice(record);
  }

  window.addEventListener('focus', checkServerSession);
  setInterval(checkServerSession, 60000);

  // Distributor reply: text is saved in the Sheet and any attached image is hosted on ImgBB.
  async function sendDistributorReply() {
    const fileInput = document.getElementById('distScreenshotInput');
    const messageInput = document.getElementById('distReplyMessage');
    const statusDiv = document.getElementById('screenshotUploadStatus');
    const file = fileInput.files[0];
    const replyMessage = messageInput.value.trim();

    if (!file && !replyMessage) {
      alert('कृपया मैसेज लिखें या इमेज/स्क्रीनशॉट सेलेक्ट करें!');
      return;
    }

    statusDiv.innerText = '⏳ Reply भेजा जा रहा है...';
    statusDiv.style.color = '#fbbf24';
    statusDiv.style.display = 'block';

    try {
      const targetEmail = currentLoggedDistributorEmail || (loginEmail.value || "").trim().toLowerCase();
      if (!targetEmail) {
        statusDiv.innerText = '⚠️ Error: Login email not found!';
        statusDiv.style.color = '#ef4444';
        return;
      }

      const imageData = file ? await preparePaymentScreenshot(file) : '';
      const result = await callCloudPost({
        action: 'replyToAdmin',
        email: targetEmail,
        message: replyMessage,
        imageData,
        fileName: file?.name || ''
      });

      if (result) {
        statusDiv.innerText = '✅ आपका reply admin को भेज दिया गया है!';
        statusDiv.style.color = '#34d399';
        fileInput.value = '';
        messageInput.value = '';
      } else {
        statusDiv.innerText = '⚠️ Reply भेजने में समस्या हुई। कृपया पुनः प्रयास करें।';
        statusDiv.style.color = '#ef4444';
      }
    } catch (err) {
      statusDiv.innerText = `⚠️ Reply भेजने में समस्या हुई: ${err?.message || err}`;
      statusDiv.style.color = '#ef4444';
    }
  }



  const loginScreen = document.getElementById('loginScreen');
  const signUpScreen = document.getElementById('signUpScreen');
  const renewalScreen = document.getElementById('renewalScreen');
  const changePwdScreen = document.getElementById('changePwdScreen');
  const mainApp = document.getElementById('mainApp');
  
  const loginEmail = document.getElementById('loginEmail');
  const loginPass = document.getElementById('loginPass');
  const authBtn = document.getElementById('authBtn');
  const errorMsg = document.getElementById('errorMsg');
  const logoutBtn = document.getElementById('logoutBtn');
  const adminTabBtn = document.getElementById('adminTabBtn');

  const goToSignUp = document.getElementById('goToSignUp');
  const signUpName = document.getElementById('signUpName');
  const signUpEmail = document.getElementById('signUpEmail');
  const signUpPass = document.getElementById('signUpPass');
  const signUpConfirmPass = document.getElementById('signUpConfirmPass');
  const signUpTxnId = document.getElementById('signUpTxnId');
  const signUpPaymentScreenshot = document.getElementById('signUpPaymentScreenshot');
  const paymentQrImage = document.getElementById('paymentQrImage');
  const paymentQrPlanText = document.getElementById('paymentQrPlanText');
  const paymentQrNote = document.getElementById('paymentQrNote');
  const paymentLinkButton = document.getElementById('paymentLinkButton');
  const signUpBtn = document.getElementById('signUpBtn');
  const signUpStatusMsg = document.getElementById('signUpStatusMsg');
  const backToLoginFromSignUp = document.getElementById('backToLoginFromSignUp');
  const renewalTxnId = document.getElementById('renewalTxnId');
  const renewalPaymentScreenshot = document.getElementById('renewalPaymentScreenshot');
  const renewalPaymentLink = document.getElementById('renewalPaymentLink');
  const renewalStatusMsg = document.getElementById('renewalStatusMsg');
  const submitRenewalBtn = document.getElementById('submitRenewalBtn');
  const backToLoginFromRenewal = document.getElementById('backToLoginFromRenewal');
  let currentRenewalDistributor = null;
  let activeDistributorSession = null;
  let renewalSubmitting = false;

  const goToChangePwd = document.getElementById('goToChangePwd');
  const backToLogin = document.getElementById('backToLogin');
  const pwdEmailInput = document.getElementById('pwdEmailInput');
  const oldPassInput = document.getElementById('oldPassInput');
  const newPassInput = document.getElementById('newPassInput');
  const confirmPassInput = document.getElementById('confirmPassInput');
  const saveNewPwdBtn = document.getElementById('saveNewPwdBtn');
  const pwdStatusMsg = document.getElementById('pwdStatusMsg');

  sessionStorage.removeItem('isLoggedIn');

  const today = new Date();
  const curDay = String(today.getDate()).padStart(2, '0');
  const curMonth = String(today.getMonth() + 1).padStart(2, '0');
  const curYear = today.getFullYear();
  document.getElementById('candDopInput').value = `DOP: ${curDay}/${curMonth}/${curYear}`;

  goToSignUp.addEventListener('click', () => {
    loginScreen.style.display = 'none';
    signUpScreen.style.display = 'block';
    changePwdScreen.style.display = 'none';
    signUpStatusMsg.style.display = 'none';
    signUpName.value = '';
    signUpEmail.value = '';
    signUpPass.value = '';
    signUpConfirmPass.value = '';
  });

  backToLoginFromSignUp.addEventListener('click', () => {
    signUpScreen.style.display = 'none';
    loginScreen.style.display = 'block';
    errorMsg.style.display = 'none';
    signUpStatusMsg.style.display = 'none';
  });

  function updateRenewalPlanUi() {
    const selected = document.querySelector('input[name="renewalPlanType"]:checked')?.value || '1month';
    const isYearly = selected === '1year';
    renewalPaymentLink.href = isYearly ? 'https://i.ibb.co/yB6gYBSL/qr-1year-319-png.jpg' : 'https://i.ibb.co/LWVdcR0/qr-1month-36-png.jpg';
    renewalPaymentLink.innerText = isYearly ? '💳 Open ₹319 Payment Link' : '💳 Open ₹36 Payment Link';
  }

  function showRenewalScreen(distributor) {
    currentRenewalDistributor = distributor;
    activeDistributorSession = null;
    currentLoggedDistributorEmail = '';
    sessionStorage.removeItem('isLoggedIn');
    const existingPlan = String(distributor.paymentPlan || '').toLowerCase();
    document.querySelector(`input[name="renewalPlanType"][value="${existingPlan.includes('year') ? '1year' : '1month'}"]`).checked = true;
    document.getElementById('renewalGreeting').innerText = `${distributor.name || 'Distributor'}, आपकी validity समाप्त हो गई है। Payment के बाद admin approval मिलने पर portal फिर से चालू होगा।`;
    renewalTxnId.value = '';
    renewalPaymentScreenshot.value = '';
    const pending = String(distributor.renewalRequested).toLowerCase() === 'true';
    submitRenewalBtn.disabled = pending;
    document.querySelectorAll('input[name="renewalPlanType"]').forEach(radio => radio.disabled = pending);
    renewalTxnId.disabled = pending;
    renewalPaymentScreenshot.disabled = pending;
    renewalStatusMsg.style.display = pending ? 'block' : 'none';
    renewalStatusMsg.style.color = '#fbbf24';
    renewalStatusMsg.innerText = '⏳ Renewal admin approval की प्रतीक्षा में है। Approval के बाद दोबारा login करें।';
    updateRenewalPlanUi();
    loginScreen.style.display = 'none';
    signUpScreen.style.display = 'none';
    changePwdScreen.style.display = 'none';
    mainApp.style.display = 'none';
    document.getElementById('pendingScreen').style.display='none';
    renewalScreen.style.display = 'block';
  }

  document.querySelectorAll('input[name="renewalPlanType"]').forEach(radio => radio.addEventListener('change', updateRenewalPlanUi));
  backToLoginFromRenewal.addEventListener('click', () => {
    renewalScreen.style.display = 'none';
    loginScreen.style.display = 'block';
    currentRenewalDistributor = null;
  });

  submitRenewalBtn.addEventListener('click', async () => {
    if (renewalSubmitting || submitRenewalBtn.disabled) return;
    const txnId = renewalTxnId.value.trim();
    const file = renewalPaymentScreenshot.files[0];
    const selectedPlan = document.querySelector('input[name="renewalPlanType"]:checked')?.value || '1month';
    if (!currentRenewalDistributor || !txnId || !file) {
      renewalStatusMsg.innerText = '⚠️ Transaction ID और payment screenshot दोनों जरूरी हैं।';
      renewalStatusMsg.style.color = '#ef4444'; renewalStatusMsg.style.display = 'block'; return;
    }
    renewalSubmitting = true;
    submitRenewalBtn.disabled = true;
    renewalStatusMsg.innerText = '⏳ Renewal request भेजी जा रही है...';
    renewalStatusMsg.style.color = '#fbbf24'; renewalStatusMsg.style.display = 'block';
    try {
      const imageData = await preparePaymentScreenshot(file);
      const plan = PAYMENT_PLAN_OPTIONS[selectedPlan];
      const result = await callRenewalPost({ action: 'submitRenewal', email: currentRenewalDistributor.email, renewalPlan: plan.label, renewalAmount: plan.amount, renewalTxnId: txnId, imageData });
      if (!result) throw new Error('Renewal request could not be saved.');
      currentRenewalDistributor.renewalRequested = 'true';
      showRenewalScreen(currentRenewalDistributor);
      renewalStatusMsg.innerText = '✅ Renewal request admin को भेज दी गई है। Approval के बाद portal चालू होगा।';
      renewalStatusMsg.style.color = '#34d399';
    } catch (err) {
      renewalStatusMsg.innerText = `⚠️ Renewal request भेजने में समस्या हुई: ${err?.message || err}`;
      renewalStatusMsg.style.color = '#ef4444';
      submitRenewalBtn.disabled = false;
    } finally { renewalSubmitting = false; }
  });

  goToChangePwd.addEventListener('click', () => {
    loginScreen.style.display = 'none';
    signUpScreen.style.display = 'none';
    changePwdScreen.style.display = 'block';
    pwdEmailInput.value = '';
    oldPassInput.value = '';
    newPassInput.value = '';
    confirmPassInput.value = '';
    pwdStatusMsg.style.display = 'none';
  });

  backToLogin.addEventListener('click', () => {
    changePwdScreen.style.display = 'none';
    signUpScreen.style.display = 'none';
    loginScreen.style.display = 'block';
    errorMsg.style.display = 'none';
  });

  function readFileAsDataURL(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => resolve(e.target.result);
      reader.onerror = () => reject(new Error('Unable to read file'));
      reader.readAsDataURL(file);
    });
  }

  function preparePaymentScreenshot(file) {
    return new Promise((resolve, reject) => {
      if (!file || !/^image\/(jpeg|jpg|png|webp)$/i.test(file.type)) {
        reject(new Error('Only JPG, PNG, or WEBP screenshots are supported'));
        return;
      }
      if (file.size > 5 * 1024 * 1024) {
        reject(new Error('Screenshot must be smaller than 5 MB'));
        return;
      }
      // Send the original file directly. This avoids canvas/image decoding errors
      // on mobile screenshots and lets Apps Script convert it to a Drive link.
      const reader = new FileReader();
      reader.onload = (event) => resolve(event.target.result);
      reader.onerror = () => reject(new Error('Unable to read screenshot'));
      reader.readAsDataURL(file);
    });
  }

  function updatePaymentPlanUi() {
    const selectedPlanValue = document.querySelector('input[name="planType"]:checked')?.value || '1month';
    const isYearly = selectedPlanValue === '1year';
    const monthlyPaymentLink = 'https://i.ibb.co/LWVdcR0/qr-1month-36-png.jpg';
    const yearlyPaymentLink = 'https://i.ibb.co/yB6gYBSL/qr-1year-319-png.jpg';

    paymentQrPlanText.innerText = isYearly ? 'Payment Link for 1 Year Plan (₹319):' : 'Payment Link for 1 Month Plan (₹36):';
    paymentLinkButton.href = isYearly ? yearlyPaymentLink : monthlyPaymentLink;
    paymentLinkButton.innerText = isYearly ? '💳 Open ₹319 Payment Link' : '💳 Open ₹36 Payment Link';
    paymentQrNote.innerText = isYearly
      ? 'Click the button above to open the ₹319 payment link.'
      : 'Click the button above to open the ₹36 payment link.';
  }

  document.querySelectorAll('input[name="planType"]').forEach((radio) => {
    radio.addEventListener('change', updatePaymentPlanUi);
  });

  updatePaymentPlanUi();

  async function handleSignUp() {
    if (authRole === 'admin') { alert('Logout before public signup.'); return; }
    clearAuth();
    const name = signUpName.value.trim();
    const email = signUpEmail.value.trim().toLowerCase();
    const pass = signUpPass.value;
    const confirmPass = signUpConfirmPass.value;
    const txnId = signUpTxnId.value.trim();
    const paymentFile = signUpPaymentScreenshot.files[0];
    const selectedPlanValue = document.querySelector('input[name="planType"]:checked')?.value || '1month';
    const selectedPlan = PAYMENT_PLAN_OPTIONS[selectedPlanValue] || PAYMENT_PLAN_OPTIONS['1month'];

    if (!name || !email || !pass || !confirmPass || !txnId) {
      signUpStatusMsg.innerText = '⚠️ कृपया सभी फ़ील्ड भरें!';
      signUpStatusMsg.style.color = '#ef4444';
      signUpStatusMsg.style.display = 'block';
      return;
    }

    if (!paymentFile) {
      signUpStatusMsg.innerText = '⚠️ कृपया भुगतान का स्क्रीनशॉट अपलोड करें!';
      signUpStatusMsg.style.color = '#ef4444';
      signUpStatusMsg.style.display = 'block';
      return;
    }

    if (email === ADMIN_EMAIL.toLowerCase()) {
      signUpStatusMsg.innerText = '⚠️ यह एडमिन ईमेल है, कृपया दूसरा ईमेल चुनें!';
      signUpStatusMsg.style.color = '#ef4444';
      signUpStatusMsg.style.display = 'block';
      return;
    }

    if (pass.length < 12) {
      signUpStatusMsg.innerText = '❌ पासवर्ड कम से कम 12 अक्षर का होना चाहिए!';
      signUpStatusMsg.style.color = '#ef4444';
      signUpStatusMsg.style.display = 'block';
      return;
    }

    if (pass !== confirmPass) {
      signUpStatusMsg.innerText = '❌ पासवर्ड और कन्फर्म पासवर्ड मेल नहीं खा रहे हैं!';
      signUpStatusMsg.style.color = '#ef4444';
      signUpStatusMsg.style.display = 'block';
      return;
    }

    signUpStatusMsg.innerText = '⏳ भुगतान सत्यापन के लिए आवेदन भेजा जा रहा है...';
    signUpStatusMsg.style.color = '#fbbf24';
    signUpStatusMsg.style.display = 'block';

    let paymentScreenshot = '';
    try {
      paymentScreenshot = await preparePaymentScreenshot(paymentFile);
    } catch (err) {
      signUpStatusMsg.innerText = '⚠️ भुगतान स्क्रीनशॉट पढ़ने में समस्या हुई, कृपया पुनः प्रयास करें।';
      signUpStatusMsg.style.color = '#ef4444';
      signUpStatusMsg.style.display = 'block';
      return;
    }

    const assignedTimestamp = Date.now();
    const distExpiryTime = assignedTimestamp + selectedPlan.ms;

    const newDistData = {
      id: Date.now(),
      name: name,
      email: email,
      pass: pass,
      assignedTimestamp: assignedTimestamp,
      expiryTime: distExpiryTime,
      adminMessage: '',
      status: 'Pending',
      paymentStatus: 'Pending',
      approvalGranted: false,
      approved: false,
      accessApproved: false,
      paymentPlan: selectedPlan.label,
      paymentAmount: selectedPlan.amount,
      paymentTxnId: txnId,
      paymentScreenshot: paymentScreenshot,
      approvalNote: 'Awaiting admin review'
    };

    const success = await addDistributorCloud(newDistData);

    if (success) {
      const screenshotUploadResult = await uploadScreenshotCloud(email, paymentScreenshot, paymentFile.name);
      if (!screenshotUploadResult.success) {
        signUpStatusMsg.innerText = `⚠️ अकाउंट बन गया है, लेकिन भुगतान screenshot upload नहीं हुआ: ${screenshotUploadResult.error || 'Unknown error'}`;
        signUpStatusMsg.style.color = '#ef4444';
        signUpStatusMsg.style.display = 'block';
        return;
      }

      signUpStatusMsg.innerText = '✅ आपका आवेदन सफलतापूर्वक भेज दिया गया है। एडमिन आपके भुगतान screenshot की समीक्षा करेगा और तभी login approved होगा।';
      signUpStatusMsg.style.color = '#34d399';
      signUpStatusMsg.style.display = 'block';

      setTimeout(() => {
        signUpScreen.style.display = 'none';
        loginScreen.style.display = 'block';
        loginEmail.value = email;
        loginPass.value = '';
        signUpName.value = '';
        signUpEmail.value = '';
        signUpPass.value = '';
        signUpConfirmPass.value = '';
        signUpTxnId.value = '';
        signUpPaymentScreenshot.value = '';
        document.querySelector('input[name="planType"][value="1month"]').checked = true;
        signUpStatusMsg.style.display = 'none';
      }, 2200);
    } else {
      signUpStatusMsg.innerText = '⚠️ अकाउंट बनाने में समस्या हुई, कृपया फिर से प्रयास करें!';
      signUpStatusMsg.style.color = '#ef4444';
      signUpStatusMsg.style.display = 'block';
    }
  }

  signUpBtn.addEventListener('click', handleSignUp);
  signUpConfirmPass.addEventListener('keypress', (e) => { if (e.key === 'Enter') handleSignUp(); });

  // ==========================================================
  // ISOLATED CHANGE PASSWORD HANDLER WITH PROFESSIONAL MESSAGES
  // ==========================================================
  saveNewPwdBtn.addEventListener('click', changePasswordFromForm);



  function enforceSessionExpiry() {
    if (!activeDistributorSession) return;
    if (Date.now() >= authExpires) { checkServerSession(); return; }
    const expiry = Number(activeDistributorSession.expiryTime || (Number(activeDistributorSession.assignedTimestamp) + THIRTY_MS));
    if (!Number.isFinite(expiry) || Date.now() >= expiry) showRenewalScreen(activeDistributorSession);
  }
  setInterval(enforceSessionExpiry, 1000);
  document.addEventListener('visibilitychange', enforceSessionExpiry);
  window.addEventListener('focus', enforceSessionExpiry);



  document.getElementById('pendingUploadBtn').addEventListener('click', async () => {
    const button=document.getElementById('pendingUploadBtn');button.disabled=true;
    try {
      const file=document.getElementById('pendingScreenshot').files[0];
      if(!file) throw new Error('Choose a screenshot.');
      const imageData=await preparePaymentScreenshot(file);
      await secureApi({action:'uploadPaymentScreenshot',imageData});
      document.getElementById('pendingStatus').textContent='Screenshot saved. Awaiting admin approval.';
    } catch(error) {document.getElementById('pendingStatus').textContent=error.message;}
    finally {button.disabled=false;}
  });
  document.getElementById('pendingBackBtn').addEventListener('click', () => {
    secureApi({action:'logout'}).catch(()=>{});clearAuth();
    document.getElementById('pendingScreen').style.display='none';loginScreen.style.display='block';
  });

  document.getElementById('adminUnlockForm').addEventListener('submit',submitAdminUnlock);
  document.getElementById('adminUnlockCancel').addEventListener('click',()=>finishAdminUnlock(false));
  document.getElementById('adminUnlockPassword').addEventListener('keydown',event=>{if(event.key==='Escape')finishAdminUnlock(false);});
  document.getElementById('lockAdminPanelBtn').addEventListener('click',lockAdminPanel);
  setInterval(()=>{if(adminPanelUntil && Date.now()>=adminPanelUntil)lockAdminPanel();},1000);
  authBtn.addEventListener('click', handleLogin);
  loginPass.addEventListener('keypress', (e) => { if (e.key === 'Enter') handleLogin(); });

  logoutBtn.addEventListener('click', () => {
    setTimeout(() => location.reload(), 100);
    secureApi({action:'logout'}).catch(() => {});
    clearAuth();
    document.getElementById('pendingScreen').style.display='none';
    sessionStorage.removeItem('isLoggedIn');
    mainApp.style.display = 'none';
    renewalScreen.style.display = 'none';
    changePwdScreen.style.display = 'none';
    loginScreen.style.display = 'block';
    loginPass.value = '';
    currentLoggedDistributorEmail = "";
    if (adminTabBtn) adminTabBtn.style.display = 'none';
    const topNavReg = document.getElementById('topNavRegistrationBox');
    if (topNavReg) topNavReg.style.display = 'flex';
  });

  // ==========================================
  // CROPPING ENGINE (Universal & Manual)
  // ==========================================
  let cropper = null;
  let activeCropType = 'card_front';
  let rawNamePassportImg = null;
  let frontCardRawData = null;
  let backCardRawData = null;

  const cropModal = document.getElementById('cropModal');
  const imageToCrop = document.getElementById('imageToCrop');
  const cropSaveBtn = document.getElementById('cropSaveBtn');
  const cropCancelBtn = document.getElementById('cropCancelBtn');

  function openCropEngine(fileOrDataUrl, type) {
    activeCropType = type;
    
    const handleLoadedImage = (src) => {
      imageToCrop.src = src;
      cropModal.style.display = 'flex';
      if (cropper) cropper.destroy();

      let targetRatio = 1013 / 638;
      if (type === 'name_passport' || type.startsWith('multi_passport_')) targetRatio = 35 / 45;
      if (type === 'photo4x6') targetRatio = 1200 / 1800;

      cropper = new Cropper(imageToCrop, {
        aspectRatio: targetRatio,
        viewMode: 1,
        autoCropArea: 0.98
      });
    };

    if (typeof fileOrDataUrl === 'string') {
      handleLoadedImage(fileOrDataUrl);
    } else {
      const reader = new FileReader();
      reader.onload = function(e) {
        handleLoadedImage(e.target.result);
      };
      reader.readAsDataURL(fileOrDataUrl);
    }
  }

  function autoFitCardToCanvas(dataUrl, targetCanvas, ctx, isFront) {
    const img = new Image();
    img.onload = function() {
      ctx.clearRect(0, 0, CARD_W, CARD_H);

      const srcRatio = img.width / img.height;
      const targetRatio = CARD_W / CARD_H;
      let sX = 0, sY = 0, sW = img.width, sH = img.height;

      if (srcRatio > targetRatio) {
        sW = img.height * targetRatio;
        sX = (img.width - sW) / 2;
      } else {
        sH = img.width / targetRatio;
        sY = (img.height - sH) / 2;
      }

      ctx.drawImage(img, sX, sY, sW, sH, 0, 0, CARD_W, CARD_H);

      if (isFront) {
        img1Loaded = true;
        frontCardRawData = dataUrl;
        document.getElementById('manualCropFrontBtn').style.display = 'inline-block';
      } else {
        img2Loaded = true;
        backCardRawData = dataUrl;
        document.getElementById('manualCropBackBtn').style.display = 'inline-block';
      }

      if (img1Loaded && img2Loaded) {
        addCardBtn.disabled = false;
      }
    };
    img.src = dataUrl;
  }

  function openManualCropForCard(side) {
    if (side === 'front' && frontCardRawData) {
      openCropEngine(frontCardRawData, 'card_front');
    } else if (side === 'back' && backCardRawData) {
      openCropEngine(backCardRawData, 'card_back');
    }
  }

  cropSaveBtn.addEventListener('click', () => {
    if (!cropper) return;

    if (activeCropType === 'card_front' || activeCropType === 'card_back') {
      const croppedCanvas = cropper.getCroppedCanvas({ width: 1013, height: 638, imageSmoothingQuality: 'high' });
      if (activeCropType === 'card_front') {
        ctx1.clearRect(0, 0, CARD_W, CARD_H);
        ctx1.drawImage(croppedCanvas, 0, 0);
        img1Loaded = true;
      } else {
        ctx2.clearRect(0, 0, CARD_W, CARD_H);
        ctx2.drawImage(croppedCanvas, 0, 0);
        img2Loaded = true;
      }
      if (img1Loaded && img2Loaded) addCardBtn.disabled = false;
    } 
    else if (activeCropType.startsWith('multi_passport_')) {
      const idx = parseInt(activeCropType.split('_')[2], 10);
      const croppedCanvas = cropper.getCroppedCanvas({ width: 413, height: 531, imageSmoothingQuality: 'high' });
      multiPassportCanvases[idx] = croppedCanvas;
      multiPassportLoaded[idx] = true;
      
      const previewCanvas = document.getElementById(`multiPassPreview${idx}`);
      if (previewCanvas) {
        previewCanvas.style.display = 'block';
        const pCtx = previewCanvas.getContext('2d');
        pCtx.clearRect(0, 0, 413, 531);
        pCtx.drawImage(croppedCanvas, 0, 0);
      }
    }
    else if (activeCropType === 'name_passport') {
      rawNamePassportImg = cropper.getCroppedCanvas({ width: 413, height: 531, imageSmoothingQuality: 'high' });
      renderNamePassportPreview();
      namePassportLoaded = true;
      document.getElementById('make4x6NamePassportBtn').disabled = false;
      document.getElementById('makeA4NamePassportBtn').disabled = false;
    }
    else if (activeCropType === 'photo4x6') {
      const croppedCanvas = cropper.getCroppedCanvas({ width: 1200, height: 1800, imageSmoothingQuality: 'high' });
      ctx4x6.clearRect(0, 0, 1200, 1800);
      ctx4x6.drawImage(croppedCanvas, 0, 0);
      photo4x6Loaded = true;
      document.getElementById('downloadDirect4x6Pdf').disabled = false;
      document.getElementById('generateA4Custom4x6Btn').disabled = false;
    }

    closeCropper();
  });

  cropCancelBtn.addEventListener('click', closeCropper);

  function closeCropper() {
    cropModal.style.display = 'none';
    if (cropper) {
      cropper.destroy();
      cropper = null;
    }
  }

  // ==========================================
  // TAB 1: 5 CARDS SYSTEM LOGIC
  // ==========================================
  const CARD_W = 1013, CARD_H = 638, A4_W = 2480, A4_H = 3508, GAP_2_5MM_PX = 30, MAX_CARDS = 5;
  let addedCardsCount = 0, img1Loaded = false, img2Loaded = false;

  const canvas1 = document.getElementById('canvas1');
  const ctx1 = canvas1.getContext('2d');
  const canvas2 = document.getElementById('canvas2');
  const ctx2 = canvas2.getContext('2d');
  const a4Canvas = document.getElementById('a4Canvas');
  const a4Ctx = a4Canvas.getContext('2d');

  const addCardBtn = document.getElementById('addCardBtn');
  const downloadPdfBtn = document.getElementById('downloadPdfBtn');
  const resetPageBtn = document.getElementById('resetPageBtn');
  const slotCounter = document.getElementById('slotCounter');

  document.getElementById('card1Input').addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
      document.getElementById('file1Name').innerText = `✅ Auto-Fitted: ${file.name}`;
      const reader = new FileReader();
      reader.onload = function(evt) {
        autoFitCardToCanvas(evt.target.result, canvas1, ctx1, true);
      };
      reader.readAsDataURL(file);
    }
  });

  document.getElementById('card2Input').addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
      document.getElementById('file2Name').innerText = `✅ Auto-Fitted: ${file.name}`;
      const reader = new FileReader();
      reader.onload = function(evt) {
        autoFitCardToCanvas(evt.target.result, canvas2, ctx2, false);
      };
      reader.readAsDataURL(file);
    }
  });

  addCardBtn.addEventListener('click', () => {
    if (addedCardsCount >= MAX_CARDS) return;
    const totalPairWidth = (CARD_W * 2) + GAP_2_5MM_PX;
    const startX = (A4_W - totalPairWidth) / 2;
    const startY = 45;
    const currentY = startY + (addedCardsCount * (CARD_H + 45));

    a4Ctx.drawImage(canvas1, startX, currentY, CARD_W, CARD_H);
    const backCardX = startX + CARD_W + GAP_2_5MM_PX;
    a4Ctx.drawImage(canvas2, backCardX, currentY, CARD_W, CARD_H);

    a4Ctx.strokeStyle = '#000000';
    a4Ctx.lineWidth = 6;
    a4Ctx.strokeRect(startX, currentY, CARD_W, CARD_H);
    a4Ctx.strokeRect(backCardX, currentY, CARD_W, CARD_H);

    addedCardsCount++;
    if (addedCardsCount < MAX_CARDS) {
      slotCounter.innerText = `Cards on Page: ${addedCardsCount} / ${MAX_CARDS} (Next Slot: #${addedCardsCount + 1})`;
    } else {
      slotCounter.innerText = `✅ Page Full: 5 / 5 Cards Added!`;
    }

    downloadPdfBtn.disabled = false;
    clearCurrentCardInputs();
  });

  function clearCurrentCardInputs() {
    [ctx1, ctx2].forEach((ctx, i) => {
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(0, 0, CARD_W, CARD_H);
      ctx.fillStyle = '#94a3b8';
      ctx.font = 'bold 24px Poppins';
      ctx.textAlign = 'center';
      ctx.fillText(`${i === 0 ? 'Front' : 'Back'} Card Preview`, CARD_W / 2, CARD_H / 2);
    });
    document.getElementById('file1Name').innerText = 'इमेज चुनें (Auto-Crop)';
    document.getElementById('file2Name').innerText = 'इमेज चुनें (Auto-Crop)';
    document.getElementById('card1Input').value = '';
    document.getElementById('card2Input').value = '';
    document.getElementById('manualCropFrontBtn').style.display = 'none';
    document.getElementById('manualCropBackBtn').style.display = 'none';
    img1Loaded = false; img2Loaded = false; addCardBtn.disabled = true;
    frontCardRawData = null; backCardRawData = null;
  }

  function resetCardA4Sheet() {
    addedCardsCount = 0;
    a4Ctx.fillStyle = '#ffffff';
    a4Ctx.fillRect(0, 0, A4_W, A4_H);
    const totalPairWidth = (CARD_W * 2) + GAP_2_5MM_PX;
    const startX = (A4_W - totalPairWidth) / 2;
    for (let i = 0; i < MAX_CARDS; i++) {
      const currentY = 45 + (i * (CARD_H + 45));
      a4Ctx.strokeStyle = '#e2e8f0';
      a4Ctx.lineWidth = 2;
      a4Ctx.strokeRect(startX, currentY, CARD_W, CARD_H);
      a4Ctx.strokeRect(startX + CARD_W + GAP_2_5MM_PX, currentY, CARD_W, CARD_H);
    }
    slotCounter.innerText = `Cards on Page: 0 / 5 (Next Slot: #1)`;
    downloadPdfBtn.disabled = true;
  }

  resetPageBtn.addEventListener('click', () => {
    if (confirm('क्या आप A4 शीट खाली करना चाहते हैं?')) {
      resetCardA4Sheet();
      clearCurrentCardInputs();
    }
  });

  downloadPdfBtn.addEventListener('click', () => {
    const { jsPDF } = window.jspdf;
    const pdf = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });
    pdf.addImage(a4Canvas.toDataURL('image/jpeg', 1.0), 'JPEG', 0, 0, 210, 297);
    
    const fileName = `A4_Cards_Sheet_${addedCardsCount}_Cards.pdf`;
    const blob = pdf.output('blob');
    pdf.save(fileName);
    saveToHistory('ID Card Print (5-Slots)', fileName, blob, 'application/pdf');
  });

  // ==========================================================
  // TAB 2: MULTI-PHOTO UNIQUE PASSPORT GENERATOR (1 to 5 PHOTOS)
  // ==========================================================
  let activePassportCount = 1;
  let multiPassportCanvases = [];
  let multiPassportLoaded = [];

  function setPassportCount(count) {
    activePassportCount = count;
    for (let i = 1; i <= 5; i++) {
      const btn = document.getElementById(`btnCount${i}`);
      if (btn) btn.style.background = '#334155';
    }
    const activeBtn = document.getElementById(`btnCount${count}`);
    if (activeBtn) activeBtn.style.background = '#0284c7';
    renderPassportUploadBlocks();
  }

  function renderPassportUploadBlocks() {
    const container = document.getElementById('passportUploadBlocksContainer');
    if (!container) return;
    container.innerHTML = '';
    multiPassportCanvases = new Array(activePassportCount);
    multiPassportLoaded = new Array(activePassportCount).fill(false);

    for (let i = 0; i < activePassportCount; i++) {
      const box = document.createElement('div');
      box.style.cssText = "flex: 1; min-width: 140px; background: rgba(15,23,42,0.8); border: 1px solid var(--border-color); padding: 10px; border-radius: 10px; text-align: center;";
      
      box.innerHTML = `
        <h5 style="font-size: 11px; color: var(--accent-blue); margin-bottom: 6px;">Photo #${i + 1}</h5>
        <canvas id="multiPassPreview${i}" width="413" height="531" style="width: 85px; height: 110px; display:none; margin: 0 auto 6px auto; background:#fff; border-radius:4px;"></canvas>
        <label class="action-btn btn-add" style="display: block; padding: 6px; font-size: 11px; cursor: pointer;">
          📁 Select Photo
          <input type="file" accept="image/*" style="display:none;" onchange="handleMultiPassportUpload(event, ${i})">
        </label>
      `;
      container.appendChild(box);
    }
  }

  function handleMultiPassportUpload(event, index) {
    const file = event.target.files[0];
    if (file) {
      openCropEngine(file, `multi_passport_${index}`);
    }
  }

  function setPassportQty(qty) {
    document.getElementById('passportQtyInput').value = qty;
  }

  document.getElementById('generateMultiPassportA4Btn').addEventListener('click', () => {
    for (let i = 0; i < activePassportCount; i++) {
      if (!multiPassportLoaded[i]) {
        alert(`⚠️ कृपया Photo #${i + 1} अपलोड और क्रॉप करें!`);
        return;
      }
    }

    const targetQty = Math.max(1, Math.min(50, parseInt(document.getElementById('passportQtyInput').value) || 30));
    const sheetCanvas = document.getElementById('passportSheetCanvas');
    const sheetCtx = sheetCanvas.getContext('2d');

    sheetCanvas.width = 2480;
    sheetCanvas.height = 3508;
    sheetCtx.fillStyle = '#ffffff';
    sheetCtx.fillRect(0, 0, 2480, 3508);

    const pw = 413, ph = 531;
    const startX = 75, startY = 80, gapX = 30, gapY = 40;
    const maxCols = 5;

    let photoIndexToPrint = 0;
    let placed = 0;
    for (let r = 0; r < 10; r++) {
      for (let c = 0; c < maxCols; c++) {
        if (placed >= targetQty) break;
        const x = startX + c * (pw + gapX);
        const y = startY + r * (ph + gapY);

        const currentCanvas = multiPassportCanvases[photoIndexToPrint % activePassportCount];
        sheetCtx.drawImage(currentCanvas, x, y, pw, ph);
        
        sheetCtx.strokeStyle = '#000000';
        sheetCtx.lineWidth = 2;
        sheetCtx.strokeRect(x, y, pw, ph);

        photoIndexToPrint++;
        placed++;
      }
    }

    document.getElementById('passportSheetTitle').innerText = `A4 Passport Sheet Preview (${activePassportCount} Unique Photos, Total Qty: ${targetQty})`;
    document.getElementById('downloadMultiPassportPdfBtn').disabled = false;
  });

  document.getElementById('downloadMultiPassportPdfBtn').addEventListener('click', () => {
    const sheetCanvas = document.getElementById('passportSheetCanvas');
    const targetQty = document.getElementById('passportQtyInput').value;
    
    const { jsPDF } = window.jspdf;
    const pdf = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });
    pdf.addImage(sheetCanvas.toDataURL('image/jpeg', 1.0), 'JPEG', 0, 0, 210, 297);
    
    const fileName = `Multi_Unique_Passport_${activePassportCount}_Photos_${targetQty}_Qty_A4.pdf`;
    const blob = pdf.output('blob');
    pdf.save(fileName);
    saveToHistory('Multi-Unique Passports', fileName, blob, 'application/pdf');
  });

  renderPassportUploadBlocks();

  // ==========================================
  // TAB 3: NAME & DATE PASSPORT (3 FONT SLIDERS)
  // ==========================================
  const namePassportCanvas = document.getElementById('namePassportCanvas');
  const namePassportCtx = namePassportCanvas.getContext('2d');
  const namePassportSheetCanvas = document.getElementById('namePassportSheetCanvas');
  const namePassportSheetCtx = namePassportSheetCanvas.getContext('2d');
  const namePassportQtyInput = document.getElementById('namePassportQtyInput');
  let namePassportLoaded = false;
  let namePassportSheetFormat = '4x6';

  let currentNameFontSize = 24;
  let currentDobFontSize = 20;
  let currentDopFontSize = 20;

  function setNamePassportQty(qty) {
    namePassportQtyInput.value = qty;
  }

  function updateNameFontSize(val) {
    currentNameFontSize = parseInt(val) || 24;
    document.getElementById('nameFontLabel').innerText = `Size: ${currentNameFontSize}px`;
    renderNamePassportPreview();
  }

  function updateDobFontSize(val) {
    currentDobFontSize = parseInt(val) || 20;
    document.getElementById('dobFontLabel').innerText = `Size: ${currentDobFontSize}px`;
    renderNamePassportPreview();
  }

  function updateDopFontSize(val) {
    currentDopFontSize = parseInt(val) || 20;
    document.getElementById('dopFontLabel').innerText = `Size: ${currentDopFontSize}px`;
    renderNamePassportPreview();
  }

  document.getElementById('namePassportInput').addEventListener('change', (e) => {
    if (e.target.files[0]) {
      document.getElementById('namePassportFileName').innerText = e.target.files[0].name;
      openCropEngine(e.target.files[0], 'name_passport');
    }
  });

  function wrapNameText(context, text, maxWidth) {
    const words = text.split(' ');
    const lines = [];
    let currentLine = words[0];

    for (let i = 1; i < words.length; i++) {
      const word = words[i];
      const width = context.measureText(currentLine + " " + word).width;
      if (width < maxWidth) {
        currentLine += " " + word;
      } else {
        lines.push(currentLine);
        currentLine = word;
      }
    }
    lines.push(currentLine);
    return lines;
  }

  function renderNamePassportPreview() {
    namePassportCtx.fillStyle = '#ffffff';
    namePassportCtx.fillRect(0, 0, 413, 531);

    if (rawNamePassportImg) {
      namePassportCtx.drawImage(rawNamePassportImg, 0, 0, 413, 531);
    }

    const cName = document.getElementById('candNameInput').value.trim();
    let rawDob = document.getElementById('candDobInput').value.trim();
    let rawDop = document.getElementById('candDopInput').value.trim();

    let formattedDob = '';
    if (rawDob) {
      formattedDob = rawDob.toUpperCase().startsWith('DOB:') ? rawDob : `DOB: ${rawDob}`;
    }

    let formattedDop = '';
    if (rawDop) {
      formattedDop = rawDop.toUpperCase().startsWith('DOP:') ? rawDop : `DOP: ${rawDop}`;
    }

    if (cName || formattedDob || formattedDop) {
      namePassportCtx.font = `900 ${currentNameFontSize}px Poppins, Arial, sans-serif`;
      const nameLines = cName ? wrapNameText(namePassportCtx, cName.toUpperCase(), 390) : [];
      
      let dateLineCount = 0;
      if (formattedDob) dateLineCount++;
      if (formattedDop) dateLineCount++;

      const nameBlockHeight = nameLines.length * (currentNameFontSize + 8);
      const dobBlockHeight = formattedDob ? (currentDobFontSize + 8) : 0;
      const dopBlockHeight = formattedDop ? (currentDopFontSize + 8) : 0;
      
      const stripHeight = Math.max(120, nameBlockHeight + dobBlockHeight + dopBlockHeight + 16);
      const stripY = 531 - stripHeight;

      namePassportCtx.fillStyle = '#ffffff';
      namePassportCtx.fillRect(0, stripY, 413, stripHeight);

      namePassportCtx.strokeStyle = '#000000';
      namePassportCtx.lineWidth = 3;
      namePassportCtx.beginPath();
      namePassportCtx.moveTo(0, stripY);
      namePassportCtx.lineTo(413, stripY);
      namePassportCtx.stroke();

      namePassportCtx.fillStyle = '#000000';
      namePassportCtx.textAlign = 'center';

      let yPos = stripY + currentNameFontSize + 6;

      namePassportCtx.font = `900 ${currentNameFontSize}px Poppins, Arial, sans-serif`;
      nameLines.forEach(line => {
        namePassportCtx.fillText(line, 413 / 2, yPos);
        yPos += currentNameFontSize + 6;
      });

      if (formattedDob) {
        yPos += 2;
        namePassportCtx.font = `700 ${currentDobFontSize}px Poppins, Arial, sans-serif`;
        namePassportCtx.fillText(formattedDob, 413 / 2, yPos);
        yPos += currentDobFontSize + 6;
      }

      if (formattedDop) {
        yPos += 2;
        namePassportCtx.font = `700 ${currentDopFontSize}px Poppins, Arial, sans-serif`;
        namePassportCtx.fillText(formattedDop, 413 / 2, yPos);
      }
    }
  }

  document.getElementById('make4x6NamePassportBtn').addEventListener('click', () => {
    if (!namePassportLoaded) return;
    namePassportSheetFormat = '4x6';
    const targetQty = Math.max(1, Math.min(8, parseInt(namePassportQtyInput.value) || 8));

    namePassportSheetCanvas.width = 1800;
    namePassportSheetCanvas.height = 1200;

    namePassportSheetCtx.fillStyle = '#ffffff';
    namePassportSheetCtx.fillRect(0, 0, 1800, 1200);

    const pw = 413, ph = 531;
    const startX = 50, startY = 50, gapX = 20, gapY = 35;
    const maxCols = 4;

    let placed = 0;
    for (let r = 0; r < 2; r++) {
      for (let c = 0; c < maxCols; c++) {
        if (placed >= targetQty) break;
        const x = startX + c * (pw + gapX);
        const y = startY + r * (ph + gapY);
        namePassportSheetCtx.drawImage(namePassportCanvas, x, y, pw, ph);
        namePassportSheetCtx.strokeStyle = '#000000';
        namePassportSheetCtx.lineWidth = 2;
        namePassportSheetCtx.strokeRect(x, y, pw, ph);
        placed++;
      }
    }

    document.getElementById('namePassportSheetTitle').innerText = `Name & Date 4×6 Sheet (${targetQty} Photos Generated)`;
    document.getElementById('downloadNamePassportPdfBtn').disabled = false;
  });

  document.getElementById('makeA4NamePassportBtn').addEventListener('click', () => {
    if (!namePassportLoaded) return;
    namePassportSheetFormat = 'a4';
    const targetQty = Math.max(1, Math.min(30, parseInt(namePassportQtyInput.value) || 30));

    namePassportSheetCanvas.width = 2480;
    namePassportSheetCanvas.height = 3508;

    namePassportSheetCtx.fillStyle = '#ffffff';
    namePassportSheetCtx.fillRect(0, 0, 2480, 3508);

    const pw = 413, ph = 531;
    const startX = 75, startY = 80, gapX = 30, gapY = 40;
    const maxCols = 5;

    let placed = 0;
    for (let r = 0; r < 6; r++) {
      for (let c = 0; c < maxCols; c++) {
        if (placed >= targetQty) break;
        const x = startX + c * (pw + gapX);
        const y = startY + r * (ph + gapY);
        namePassportSheetCtx.drawImage(namePassportCanvas, x, y, pw, ph);
        namePassportSheetCtx.strokeStyle = '#000000';
        namePassportSheetCtx.lineWidth = 2;
        namePassportSheetCtx.strokeRect(x, y, pw, ph);
        placed++;
      }
    }

    document.getElementById('namePassportSheetTitle').innerText = `Name & Date A4 Sheet (${targetQty} Photos Generated)`;
    document.getElementById('downloadNamePassportPdfBtn').disabled = false;
  });

  document.getElementById('downloadNamePassportPdfBtn').addEventListener('click', () => {
    const { jsPDF } = window.jspdf;
    let fileName = '';
    let pdf;
    if (namePassportSheetFormat === '4x6') {
      pdf = new jsPDF({ orientation: 'landscape', unit: 'in', format: [4, 6] });
      pdf.addImage(namePassportSheetCanvas.toDataURL('image/jpeg', 1.0), 'JPEG', 0, 0, 6, 4);
      fileName = `Name_Date_Passport_4x6_${namePassportQtyInput.value}_Qty.pdf`;
    } else {
      pdf = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });
      pdf.addImage(namePassportSheetCanvas.toDataURL('image/jpeg', 1.0), 'JPEG', 0, 0, 210, 297);
      fileName = `Name_Date_Passport_A4_${namePassportQtyInput.value}_Qty.pdf`;
    }
    const blob = pdf.output('blob');
    pdf.save(fileName);
    saveToHistory('Name & Date Passport', fileName, blob, 'application/pdf');
  });

  // ==========================================
  // TAB 4: 4x6 PHOTO PRINT
  // ==========================================
  const canvas4x6 = document.getElementById('canvas4x6');
  const ctx4x6 = canvas4x6.getContext('2d');
  const a4_4x6_SheetCanvas = document.getElementById('a4_4x6_SheetCanvas');
  const a4_4x6_SheetCtx = a4_4x6_SheetCanvas.getContext('2d');
  const photo4x6QtyInput = document.getElementById('photo4x6QtyInput');
  let photo4x6Loaded = false;

  function set4x6Qty(qty) {
    photo4x6QtyInput.value = qty;
  }

  document.getElementById('photo4x6Input').addEventListener('change', (e) => {
    if (e.target.files[0]) {
      document.getElementById('photo4x6FileName').innerText = e.target.files[0].name;
      openCropEngine(e.target.files[0], 'photo4x6');
    }
  });

  document.getElementById('downloadDirect4x6Pdf').addEventListener('click', () => {
    if (!photo4x6Loaded) return;
    const { jsPDF } = window.jspdf;
    const pdf = new jsPDF({ orientation: 'portrait', unit: 'in', format: [4, 6] });
    pdf.addImage(canvas4x6.toDataURL('image/jpeg', 1.0), 'JPEG', 0, 0, 4, 6);
    const fileName = 'Photo_4x6_Print.pdf';
    const blob = pdf.output('blob');
    pdf.save(fileName);
    saveToHistory('4x6 Photo (Single)', fileName, blob, 'application/pdf');
  });

  document.getElementById('generateA4Custom4x6Btn').addEventListener('click', () => {
    if (!photo4x6Loaded) return;
    const qty = Math.max(1, Math.min(4, parseInt(photo4x6QtyInput.value) || 2));

    a4_4x6_SheetCanvas.width = 2480;
    a4_4x6_SheetCanvas.height = 3508;

    a4_4x6_SheetCtx.fillStyle = '#ffffff';
    a4_4x6_SheetCtx.fillRect(0, 0, 2480, 3508);

    const pw = 1140, ph = 1680;
    const gapX = 60, gapY = 60;
    const startX = 70, startY = 40;

    const positions = [
      { x: startX, y: startY },
      { x: startX + pw + gapX, y: startY },
      { x: startX, y: startY + ph + gapY },
      { x: startX + pw + gapX, y: startY + ph + gapY }
    ];

    for (let i = 0; i < qty; i++) {
      const pos = positions[i];
      a4_4x6_SheetCtx.drawImage(canvas4x6, pos.x, pos.y, pw, ph);
      a4_4x6_SheetCtx.strokeStyle = '#000000';
      a4_4x6_SheetCtx.lineWidth = 4;
      a4_4x6_SheetCtx.strokeRect(pos.x, pos.y, pw, ph);
    }

    document.getElementById('photo4x6SheetTitle').innerText = `A4 4×6 Photo Sheet (${qty} Photos on 1 A4)`;
    document.getElementById('downloadA4_4x6_PdfBtn').disabled = false;
  });

  document.getElementById('downloadA4_4x6_PdfBtn').addEventListener('click', () => {
    const { jsPDF } = window.jspdf;
    const pdf = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });
    pdf.addImage(a4_4x6_SheetCanvas.toDataURL('image/jpeg', 1.0), 'JPEG', 0, 0, 210, 297);
    const fileName = `4x6_Photos_A4_Sheet_${photo4x6QtyInput.value}_Qty.pdf`;
    const blob = pdf.output('blob');
    pdf.save(fileName);
    saveToHistory('4x6 Photo A4 Sheet', fileName, blob, 'application/pdf');
  });

  // ==========================================================
  // TAB 5: PDF ARRANGER (DRAG & DROP / HOLD & MOVE)
  // ==========================================================
  let arrangedPdfPagesList = [];
  let draggedArrangerIdx = null;

  document.getElementById('arrangerPdfInput').addEventListener('change', async function(e) {
    const files = Array.from(e.target.files);
    if (!files.length) return;

    for (const file of files) {
      const arrayBuffer = await file.arrayBuffer();
      const pdf = await pdfjsLib.getDocument({ isEvalSupported: false, enableScripting: false, data: new Uint8Array(arrayBuffer) }).promise;

      for (let i = 1; i <= pdf.numPages; i++) {
        const page = await pdf.getPage(i);
        const viewport = page.getViewport({ scale: 0.35 });

        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = viewport.width;
        canvas.height = viewport.height;

        await page.render({ canvasContext: ctx, viewport: viewport }).promise;

        arrangedPdfPagesList.push({
          sourceBytes: arrayBuffer,
          pageIndex: i - 1,
          thumbDataUrl: canvas.toDataURL('image/jpeg', 0.8),
          rotation: 0,
          originalDocName: file.name
        });
      }
    }

    renderArrangerGrid();
    this.value = '';
  });

  function renderArrangerGrid() {
    const grid = document.getElementById('arrangerGridList');
    const container = document.getElementById('arrangerContainerArea');
    const countDisplay = document.getElementById('arrangerTotalPagesCount');

    grid.innerHTML = '';
    countDisplay.innerText = arrangedPdfPagesList.length;

    if (arrangedPdfPagesList.length > 0) {
      container.style.display = 'block';
    } else {
      container.style.display = 'none';
      return;
    }

    arrangedPdfPagesList.forEach((item, idx) => {
      const card = document.createElement('div');
      card.className = 'draggable-card';
      card.draggable = true;
      card.dataset.index = idx;

      card.addEventListener('dragstart', (e) => {
        draggedArrangerIdx = idx;
        card.classList.add('dragging');
        e.dataTransfer.effectAllowed = 'move';
      });

      card.addEventListener('dragend', () => {
        card.classList.remove('dragging');
        document.querySelectorAll('.draggable-card').forEach(c => c.classList.remove('drag-over'));
      });

      card.addEventListener('dragover', (e) => {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
        card.classList.add('drag-over');
      });

      card.addEventListener('dragleave', () => {
        card.classList.remove('drag-over');
      });

      card.addEventListener('drop', (e) => {
        e.preventDefault();
        card.classList.remove('drag-over');
        if (draggedArrangerIdx !== null && draggedArrangerIdx !== idx) {
          const itemToMove = arrangedPdfPagesList.splice(draggedArrangerIdx, 1)[0];
          arrangedPdfPagesList.splice(idx, 0, itemToMove);
          renderArrangerGrid();
        }
      });

      const img = document.createElement('img');
      img.src = item.thumbDataUrl;
      img.style.transform = `rotate(${item.rotation}deg)`;
      card.appendChild(img);

      const label = document.createElement('div');
      label.className = 'file-label';
      label.innerText = `Page ${idx + 1}`;
      card.appendChild(label);

      const toolsBar = document.createElement('div');
      toolsBar.className = 'card-tools-bar';

      const rotateBtn = document.createElement('button');
      rotateBtn.className = 'mini-tool-btn';
      rotateBtn.innerHTML = '🔄 Rotate';
      rotateBtn.title = 'Rotate 90°';
      rotateBtn.onclick = (e) => {
        e.stopPropagation();
        rotateArrangerPage(idx);
      };

      const delBtn = document.createElement('button');
      delBtn.className = 'mini-tool-btn btn-del';
      delBtn.innerHTML = '🗑️';
      delBtn.title = 'Delete Page';
      delBtn.onclick = (e) => {
        e.stopPropagation();
        deleteArrangerPage(idx);
      };

      toolsBar.appendChild(rotateBtn);
      toolsBar.appendChild(delBtn);
      card.appendChild(toolsBar);

      grid.appendChild(card);
    });
  }

  function rotateArrangerPage(index) {
    arrangedPdfPagesList[index].rotation = (arrangedPdfPagesList[index].rotation + 90) % 360;
    renderArrangerGrid();
  }

  function deleteArrangerPage(index) {
    arrangedPdfPagesList.splice(index, 1);
    renderArrangerGrid();
  }

  document.getElementById('clearArrangerBtn').addEventListener('click', () => {
    if (confirm('क्या आप सभी अरेंज किए गए पेज मिटाना चाहते हैं?')) {
      arrangedPdfPagesList = [];
      renderArrangerGrid();
    }
  });

  document.getElementById('saveArrangedPdfBtn').addEventListener('click', async () => {
    if (!arrangedPdfPagesList.length) return;

    const { PDFDocument, degrees } = PDFLib;
    const outPdf = await PDFDocument.create();

    const loadedDocsMap = new Map();

    for (const pageObj of arrangedPdfPagesList) {
      let srcDoc = loadedDocsMap.get(pageObj.sourceBytes);
      if (!srcDoc) {
        srcDoc = await PDFDocument.load(pageObj.sourceBytes);
        loadedDocsMap.set(pageObj.sourceBytes, srcDoc);
      }

      const [copiedPage] = await outPdf.copyPages(srcDoc, [pageObj.pageIndex]);
      
      if (pageObj.rotation !== 0) {
        const currentRot = copiedPage.getRotation().angle;
        copiedPage.setRotation(degrees(currentRot + pageObj.rotation));
      }

      outPdf.addPage(copiedPage);
    }

    const pdfBytes = await outPdf.save();
    const blob = new Blob([pdfBytes], { type: 'application/pdf' });
    const fileName = `Arranged_Document_${arrangedPdfPagesList.length}_Pages.pdf`;

    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = fileName;
    link.click();
    saveToHistory('PDF Arranger', fileName, blob, 'application/pdf');
  });

  // ==========================================================
  // TAB 6: UNIVERSAL MERGE (DRAG & DROP RE-ORDER SUPPORT)
  // ==========================================================
  let universalFiles = [];
  let draggedUniversalIdx = null;

  document.getElementById('universalMultiInput').addEventListener('change', function(e) {
    const files = Array.from(e.target.files);
    if (!files.length) return;

    universalFiles = universalFiles.concat(files);
    renderUniversalGallery();
    this.value = '';
  });

  function removeUniversalFile(index) {
    universalFiles.splice(index, 1);
    renderUniversalGallery();
  }

  function renderUniversalGallery() {
    const gallery = document.getElementById('universalGalleryList');
    const container = document.getElementById('universalGalleryContainer');
    const countDisplay = document.getElementById('universalSelectedCount');

    gallery.innerHTML = '';
    countDisplay.innerText = universalFiles.length;

    if (universalFiles.length > 0) {
      container.style.display = 'block';
    } else {
      container.style.display = 'none';
      return;
    }

    universalFiles.forEach((file, idx) => {
      const item = document.createElement('div');
      item.className = 'draggable-card';
      item.draggable = true;

      item.addEventListener('dragstart', (e) => {
        draggedUniversalIdx = idx;
        item.classList.add('dragging');
        e.dataTransfer.effectAllowed = 'move';
      });

      item.addEventListener('dragend', () => {
        item.classList.remove('dragging');
        document.querySelectorAll('#universalGalleryList .draggable-card').forEach(c => c.classList.remove('drag-over'));
      });

      item.addEventListener('dragover', (e) => {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
        item.classList.add('drag-over');
      });

      item.addEventListener('dragleave', () => {
        item.classList.remove('drag-over');
      });

      item.addEventListener('drop', (e) => {
        e.preventDefault();
        item.classList.remove('drag-over');
        if (draggedUniversalIdx !== null && draggedUniversalIdx !== idx) {
          const moved = universalFiles.splice(draggedUniversalIdx, 1)[0];
          universalFiles.splice(idx, 0, moved);
          renderUniversalGallery();
        }
      });

      const delBtn = document.createElement('button');
      delBtn.className = 'item-delete-btn';
      delBtn.innerHTML = '✖';
      delBtn.title = 'Remove this file';
      delBtn.onclick = function(e) {
        e.stopPropagation();
        removeUniversalFile(idx);
      };
      item.appendChild(delBtn);

      if (file.type === 'application/pdf') {
        const icon = document.createElement('div');
        icon.style.height = '135px';
        icon.style.display = 'flex';
        icon.style.alignItems = 'center';
        icon.style.justifyContent = 'center';
        icon.style.fontSize = '36px';
        icon.innerText = '📄';
        item.appendChild(icon);
      } else {
        const img = document.createElement('img');
        img.src = URL.createObjectURL(file);
        item.appendChild(img);
      }

      const label = document.createElement('div');
      label.className = 'file-label';
      label.innerText = file.name;
      label.title = file.name;
      item.appendChild(label);

      gallery.appendChild(item);
    });
  }

  document.getElementById('clearUniversalListBtn').addEventListener('click', () => {
    universalFiles = [];
    renderUniversalGallery();
    document.getElementById('universalMultiInput').value = '';
  });

  document.getElementById('convertUniversalToPdfBtn').addEventListener('click', async () => {
    if (!universalFiles.length) return;

    const { PDFDocument } = PDFLib;
    const mergedPdf = await PDFDocument.create();

    for (let i = 0; i < universalFiles.length; i++) {
      const file = universalFiles[i];
      const fileBytes = await file.arrayBuffer();

      if (file.type === 'application/pdf') {
        const externalPdf = await PDFDocument.load(fileBytes);
        const copiedPages = await mergedPdf.copyPages(externalPdf, externalPdf.getPageIndices());
        copiedPages.forEach((page) => mergedPdf.addPage(page));
      } else {
        let embeddedImage;
        if (file.type === 'image/png') {
          embeddedImage = await mergedPdf.embedPng(fileBytes);
        } else {
          embeddedImage = await mergedPdf.embedJpg(fileBytes);
        }

        const page = mergedPdf.addPage([595.28, 841.89]);
        const imgDims = embeddedImage.scaleToFit(555.28, 801.89);

        page.drawImage(embeddedImage, {
          x: (595.28 - imgDims.width) / 2,
          y: (841.89 - imgDims.height) / 2,
          width: imgDims.width,
          height: imgDims.height
        });
      }
    }

    const mergedPdfBytes = await mergedPdf.save();
    const blob = new Blob([mergedPdfBytes], { type: 'application/pdf' });
    const fileName = `Merged_Combined_Document.pdf`;
    
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = fileName;
    link.click();
    saveToHistory('Universal PDF Merge', fileName, blob, 'application/pdf');
  });

  // ==========================================================
  // TAB 7: CUSTOM IMAGE RESIZER
  // ==========================================================
  let originalResizerImg = null;
  let resizerOriginalWidth = 0;
  let resizerOriginalHeight = 0;
  const resizerCanvas = document.getElementById('resizerPreviewCanvas');
  const resizerCtx = resizerCanvas.getContext('2d');
  const DPI_SCALE = 300;

  document.getElementById('resizerImageInput').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (!file) return;

    document.getElementById('resizerFileName').innerText = `✅ ${file.name}`;
    const reader = new FileReader();
    reader.onload = function(evt) {
      originalResizerImg = new Image();
      originalResizerImg.onload = function() {
        resizerOriginalWidth = originalResizerImg.width;
        resizerOriginalHeight = originalResizerImg.height;

        document.getElementById('resizerUnitSelect').value = 'px';
        document.getElementById('resizerWidthInput').value = resizerOriginalWidth;
        document.getElementById('resizerHeightInput').value = resizerOriginalHeight;

        document.getElementById('resizerControlsPanel').style.display = 'block';
        updateResizerCanvas();
      };
      originalResizerImg.src = evt.target.result;
    };
    reader.readAsDataURL(file);
  });

  function getPixelDimensions() {
    const unit = document.getElementById('resizerUnitSelect').value;
    const wVal = parseFloat(document.getElementById('resizerWidthInput').value) || 1;
    const hVal = parseFloat(document.getElementById('resizerHeightInput').value) || 1;

    let targetW = wVal;
    let targetH = hVal;

    if (unit === 'mm') {
      targetW = Math.round((wVal / 25.4) * DPI_SCALE);
      targetH = Math.round((hVal / 25.4) * DPI_SCALE);
    } else if (unit === 'cm') {
      targetW = Math.round((wVal / 2.54) * DPI_SCALE);
      targetH = Math.round((hVal / 2.54) * DPI_SCALE);
    }

    return {
      width: Math.max(1, targetW),
      height: Math.max(1, targetH)
    };
  }

  function updateResizerCanvas() {
    if (!originalResizerImg) return;
    const dims = getPixelDimensions();

    resizerCanvas.width = dims.width;
    resizerCanvas.height = dims.height;

    resizerCtx.clearRect(0, 0, dims.width, dims.height);
    resizerCtx.drawImage(originalResizerImg, 0, 0, dims.width, dims.height);

    const unit = document.getElementById('resizerUnitSelect').value;
    const wInp = document.getElementById('resizerWidthInput').value;
    const hInp = document.getElementById('resizerHeightInput').value;

    document.getElementById('resizerOutputInfo').innerText = `Target: ${wInp} x ${hInp} ${unit} (${dims.width} x ${dims.height} px)`;
  }

  function onResizerDimensionChange(changed) {
    if (!originalResizerImg) return;
    const isLocked = document.getElementById('resizerAspectLock').checked;

    if (isLocked && resizerOriginalWidth > 0 && resizerOriginalHeight > 0) {
      const ratio = resizerOriginalHeight / resizerOriginalWidth;
      if (changed === 'width') {
        const w = parseFloat(document.getElementById('resizerWidthInput').value) || 0;
        document.getElementById('resizerHeightInput').value = (w * ratio).toFixed(1);
      } else {
        const h = parseFloat(document.getElementById('resizerHeightInput').value) || 0;
        document.getElementById('resizerWidthInput').value = (h / ratio).toFixed(1);
      }
    }
    updateResizerCanvas();
  }

  function onResizerUnitChange() {
    if (!originalResizerImg) return;
    const unit = document.getElementById('resizerUnitSelect').value;

    if (unit === 'px') {
      document.getElementById('resizerWidthInput').value = resizerOriginalWidth;
      document.getElementById('resizerHeightInput').value = resizerOriginalHeight;
    } else if (unit === 'mm') {
      document.getElementById('resizerWidthInput').value = ((resizerOriginalWidth / DPI_SCALE) * 25.4).toFixed(1);
      document.getElementById('resizerHeightInput').value = ((resizerOriginalHeight / DPI_SCALE) * 25.4).toFixed(1);
    } else if (unit === 'cm') {
      document.getElementById('resizerWidthInput').value = ((resizerOriginalWidth / DPI_SCALE) * 2.54).toFixed(2);
      document.getElementById('resizerHeightInput').value = ((resizerOriginalHeight / DPI_SCALE) * 2.54).toFixed(2);
    }
    updateResizerCanvas();
  }

  document.getElementById('downloadResizedJpgBtn').addEventListener('click', () => {
    if (!originalResizerImg) return;
    const dims = getPixelDimensions();
    const dataUrl = resizerCanvas.toDataURL('image/jpeg', 0.95);
    const fileName = `Resized_${dims.width}x${dims.height}px.jpg`;
    
    const link = document.createElement('a');
    link.href = dataUrl;
    link.download = fileName;
    link.click();
    saveToHistory('Image Resizer (JPG)', fileName, dataUrl, 'image/jpeg');
  });

  document.getElementById('downloadResizedPngBtn').addEventListener('click', () => {
    if (!originalResizerImg) return;
    const dims = getPixelDimensions();
    const dataUrl = resizerCanvas.toDataURL('image/png');
    const fileName = `Resized_${dims.width}x${dims.height}px.png`;

    const link = document.createElement('a');
    link.href = dataUrl;
    link.download = fileName;
    link.click();
    saveToHistory('Image Resizer (PNG)', fileName, dataUrl, 'image/png');
  });

  // ==========================================================
  // TAB 8: PDF TO HIGH-DPI JPG CONVERTER
  // ==========================================================
  let pdfToJpgDoc = null;
  let activeDpiValue = 300;

  function setPdfDpi(dpi) {
    activeDpiValue = dpi;
    document.getElementById('manualDpiInput').value = dpi;
    document.getElementById('currentDpiDisplay').innerText = `${dpi} DPI`;
  }

  function updateManualDpi(val) {
    let dpi = parseInt(val) || 300;
    if (dpi < 50) dpi = 50;
    if (dpi > 1200) dpi = 1200;
    activeDpiValue = dpi;
    document.getElementById('currentDpiDisplay').innerText = `${dpi} DPI`;
  }

  document.getElementById('pdfToJpgInput').addEventListener('change', async function(e) {
    const file = e.target.files[0];
    if (!file) return;

    document.getElementById('pdfToJpgStatus').innerText = `✅ ${file.name}`;
    const arrayBuffer = await file.arrayBuffer();

    pdfToJpgDoc = await pdfjsLib.getDocument({ isEvalSupported: false, enableScripting: false, data: new Uint8Array(arrayBuffer) }).promise;
    document.getElementById('pdfToJpgControls').style.display = 'block';
  });

  document.getElementById('startPdfToJpgBtn').addEventListener('click', async () => {
    if (!pdfToJpgDoc) return;

    const progress = document.getElementById('pdfConversionProgress');
    const scaleFactor = activeDpiValue / 72;
    const totalPages = pdfToJpgDoc.numPages;

    if (totalPages === 1) {
      progress.innerText = `⏳ Rendering 1 page at ${activeDpiValue} DPI...`;
      const page = await pdfToJpgDoc.getPage(1);
      const viewport = page.getViewport({ scale: scaleFactor });

      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      canvas.width = viewport.width;
      canvas.height = viewport.height;

      await page.render({ canvasContext: ctx, viewport: viewport }).promise;

      canvas.toBlob((blob) => {
        const fileName = `Page_1_${activeDpiValue}DPI.jpg`;
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = fileName;
        link.click();
        progress.innerText = `✅ Download Complete (1 Page @ ${activeDpiValue} DPI)`;
        saveToHistory('PDF to JPG (Single)', fileName, blob, 'image/jpeg');
      }, 'image/jpeg', 0.95);

    } else {
      const zip = new JSZip();
      for (let i = 1; i <= totalPages; i++) {
        progress.innerText = `⏳ Processing Page ${i} / ${totalPages} at ${activeDpiValue} DPI...`;
        const page = await pdfToJpgDoc.getPage(i);
        const viewport = page.getViewport({ scale: scaleFactor });

        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = viewport.width;
        canvas.height = viewport.height;

        await page.render({ canvasContext: ctx, viewport: viewport }).promise;
        const imgData = canvas.toDataURL('image/jpeg', 0.95).split(',')[1];
        zip.file(`Page_${i}_${activeDpiValue}DPI.jpg`, imgData, { base64: true });
      }

      progress.innerText = '📦 Creating ZIP archive...';
      const zipContent = await zip.generateAsync({ type: 'blob' });
      const fileName = `PDF_to_JPG_${activeDpiValue}DPI_Bundle.zip`;
      const link = document.createElement('a');
      link.href = URL.createObjectURL(zipContent);
      link.download = fileName;
      link.click();
      progress.innerText = `✅ Complete! ${totalPages} Pages Downloaded in ZIP.`;
      saveToHistory('PDF to JPG (Batch ZIP)', fileName, zipContent, 'application/zip');
    }
  });

  // ==========================================================
  // TAB 9: PDF COMPRESSOR
  // ==========================================================
  let compressOriginalFile = null;
  let compressPdfDoc = null;
  let origFileSizeInKB = 0;

  document.getElementById('pdfCompressInput').addEventListener('change', async function(e) {
    const file = e.target.files[0];
    if (!file) return;

    compressOriginalFile = file;
    origFileSizeInKB = (file.size / 1024).toFixed(1);
    
    document.getElementById('pdfCompressStatus').innerText = `✅ ${file.name}`;
    document.getElementById('origFileSizeDisplay').innerText = formatBytes(file.size);

    const arrayBuffer = await file.arrayBuffer();
    compressPdfDoc = await pdfjsLib.getDocument({ isEvalSupported: false, enableScripting: false, data: new Uint8Array(arrayBuffer) }).promise;

    document.getElementById('compressorControlsArea').style.display = 'block';
    onCompressSliderChange(document.getElementById('compressQualitySlider').value);
  });

  function onCompressSliderChange(val) {
    const quality = parseInt(val);
    let levelText = 'Medium';
    if (quality < 35) levelText = 'High Compression (Smallest Size)';
    else if (quality > 75) levelText = 'Light Compression (High Quality)';
    
    document.getElementById('compressQualityLabel').innerText = `${quality}% (${levelText})`;

    const ratio = Math.pow(quality / 100, 1.3);
    const estBytes = compressOriginalFile.size * Math.max(0.15, ratio);
    document.getElementById('estFileSizeDisplay').innerText = formatBytes(estBytes);
  }

  function formatBytes(bytes) {
    if (bytes < 1024) return bytes + ' Bytes';
    else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
    else return (bytes / 1048576).toFixed(2) + ' MB';
  }

  document.getElementById('startCompressDownloadBtn').addEventListener('click', async () => {
    if (!compressPdfDoc) return;

    const progress = document.getElementById('compressProgressMsg');
    const qualityVal = parseInt(document.getElementById('compressQualitySlider').value);
    const jpegQuality = qualityVal / 100;
    
    const renderScale = Math.max(1.0, (qualityVal / 100) * 2.2); 
    const totalPages = compressPdfDoc.numPages;

    progress.innerText = `⏳ Compressing ${totalPages} pages...`;

    const { jsPDF } = window.jspdf;
    let outPdf = null;

    for (let i = 1; i <= totalPages; i++) {
      progress.innerText = `⏳ Compressing Page ${i} of ${totalPages}...`;
      const page = await compressPdfDoc.getPage(i);
      const viewport = page.getViewport({ scale: renderScale });

      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      canvas.width = viewport.width;
      canvas.height = viewport.height;

      await page.render({ canvasContext: ctx, viewport: viewport }).promise;
      const imgData = canvas.toDataURL('image/jpeg', jpegQuality);

      const orientation = viewport.width > viewport.height ? 'landscape' : 'portrait';
      if (i === 1) {
        outPdf = new jsPDF({ orientation: orientation, unit: 'pt', format: [viewport.width, viewport.height] });
      } else {
        outPdf.addPage([viewport.width, viewport.height], orientation);
      }

      outPdf.addImage(imgData, 'JPEG', 0, 0, viewport.width, viewport.height, undefined, 'FAST');
    }

    const fileName = `Compressed_${qualityVal}pct_${compressOriginalFile.name}`;
    const blob = outPdf.output('blob');
    progress.innerText = `✅ Compression Complete! Downloading...`;
    outPdf.save(fileName);
    saveToHistory('PDF Compressor', fileName, blob, 'application/pdf');
  });

  function initAllCanvases() {
    clearCurrentCardInputs();
    resetCardA4Sheet();

    namePassportCtx.fillStyle = '#ffffff';
    namePassportCtx.fillRect(0, 0, 413, 531);
    namePassportCtx.fillStyle = '#94a3b8';
    namePassportCtx.font = 'bold 20px Poppins';
    namePassportCtx.textAlign = 'center';
    namePassportCtx.fillText('Name & Date Preview', 413 / 2, 531 / 2);

    ctx4x6.fillStyle = '#ffffff';
    ctx4x6.fillRect(0, 0, 1200, 1800);
    ctx4x6.fillStyle = '#94a3b8';
    ctx4x6.font = 'bold 36px Poppins';
    ctx4x6.textAlign = 'center';
    ctx4x6.fillText('4×6 Photo Preview', 1200 / 2, 1800 / 2);

    a4_4x6_SheetCtx.fillStyle = '#ffffff';
    a4_4x6_SheetCtx.fillRect(0, 0, 2480, 3508);
  }
</script>

<script>
/* Local PDF annotation editor. Original PDF content is preserved, not redacted. */
(() => {
 'use strict';
 const $ = id => document.getElementById('pe-' + id);
 const root = document.getElementById('tab-pdf-editor');
 const base = $('base'), overlay = $('overlay');
 let doc=null, bytes=null, filename='', pages=[], pageIndex=0, viewport=null;
 let tool='select', selected=-1, drag=null, pendingImage=null, busy=false, epoch=0, renderSerial=0;
 let undo=[], redo=[], assets=new Map(), nextAsset=1, dirty=false;
 const clone = v => JSON.parse(JSON.stringify(v));
 const items = () => pages[pageIndex] || [];
 const number = (id,min,max) => Math.min(max,Math.max(min,Number($(id).value)||min));
 const status = message => { $('status').textContent=message; };
 function controls() {
  $('controls').disabled=!doc||busy;
  $('open').disabled=busy; $('close').disabled=!doc||busy; $('download').disabled=!doc||busy;
  $('undo').disabled=!undo.length; $('redo').disabled=!redo.length;
  $('prev').disabled=pageIndex===0; $('next').disabled=!doc||pageIndex>=doc.numPages-1;
  ['delete','smaller','larger','apply'].forEach(id=>$(id).disabled=selected<0);
  $('selection').textContent=selected<0?'No item selected':`Selected: ${items()[selected]?.type || 'item'} · ${selected+1}`;
 }
 function remember() { undo.push(clone(pages)); if(undo.length>40)undo.shift(); redo=[];dirty=true; }
 function setTool(value) {
  tool=value; selected=-1;drag=null;
  root.querySelectorAll('[data-pe-tool]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.peTool===value)));
  status(value==='select'?'अपने जोड़े हुए item पर click करके drag करें।':value==='image'?'Image लगाने के लिए page पर click करें।':`${value}: page पर click / drag करें।`);
  repaint();controls();
 }
 function style() {return {color:$('color').value,size:number('size',6,120),pen:number('pen',1,20),bold:$('bold').checked};}
 function textMetrics(o) {
  const c=overlay.getContext('2d');c.font=`${o.bold?'bold ':''}${o.size}px Arial, sans-serif`;
  o.w=Math.max(10,...o.text.split('\n').map(line=>c.measureText(line).width))+4;
  o.h=Math.max(1,o.text.split('\n').length)*o.size*1.3+4;
 }
 function drawItem(c,o) {
  c.save();c.translate(o.x,o.y);c.strokeStyle=o.color;c.fillStyle=o.color;c.lineWidth=o.pen;c.lineCap='round';c.lineJoin='round';
  if(o.type==='text') {
   c.font=`${o.bold?'bold ':''}${o.size}px Arial, sans-serif`;c.textBaseline='top';
   o.text.split('\n').forEach((line,i)=>c.fillText(line,2,2+i*o.size*1.3));
  } else if(o.type==='image') {const a=assets.get(o.asset);if(a)c.drawImage(a,0,0,o.w,o.h);}
  else if(o.type==='whiteout'){c.fillStyle='#ffffff';c.fillRect(0,0,o.w,o.h);}
  else if(o.type==='highlight'){c.globalAlpha=.32;c.fillRect(0,0,o.w,o.h);}
  else if(o.type==='rect'){c.strokeRect(0,0,o.w,o.h);}
  else if(o.type==='draw'){
   c.beginPath();o.points.forEach((p,i)=>i?c.lineTo(p[0]*o.w,p[1]*o.h):c.moveTo(p[0]*o.w,p[1]*o.h));c.stroke();
  } else if(o.type==='check') {c.lineWidth=Math.max(2,o.w/10);c.beginPath();c.moveTo(0,o.h*.5);c.lineTo(o.w*.35,o.h);c.lineTo(o.w,0);c.stroke();}
  else if(o.type==='cross'){c.lineWidth=Math.max(2,o.w/10);c.beginPath();c.moveTo(0,0);c.lineTo(o.w,o.h);c.moveTo(o.w,0);c.lineTo(0,o.h);c.stroke();}
  c.restore();
 }
 function repaint() {
  const c=overlay.getContext('2d');c.clearRect(0,0,overlay.width,overlay.height);if(!viewport)return;
  c.save();c.scale(overlay.width/viewport.width,overlay.height/viewport.height);
  items().forEach(o=>drawItem(c,o));
  if(drag?.preview)drawItem(c,drag.preview);
  const o=items()[selected];
  if(o){c.strokeStyle='#0284c7';c.lineWidth=1;c.setLineDash([4,3]);c.strokeRect(o.x-3,o.y-3,o.w+6,o.h+6);}
  c.restore();
 }
 async function renderPage() {
  if(!doc)return;
  const serial=++renderSerial, token=epoch, current=doc;
  busy=true;controls();status('Page render हो रहा है…');
  try {
   const page=await current.getPage(pageIndex+1);
   if(token!==epoch||serial!==renderSerial)return;
   const view=page.getViewport({scale:1});
   const scale=Math.min(2,3000/Math.max(view.width,view.height));
   const rendered=page.getViewport({scale});
   const temp=document.createElement('canvas');temp.width=Math.ceil(rendered.width);temp.height=Math.ceil(rendered.height);
   await page.render({canvasContext:temp.getContext('2d'),viewport:rendered}).promise;
   if(token!==epoch||serial!==renderSerial)return;
   viewport=view;base.width=temp.width;base.height=temp.height;base.getContext('2d').drawImage(temp,0,0);
   overlay.width=temp.width;overlay.height=temp.height;
   const zoom=Number($('zoom').value);const width=view.width*zoom,height=view.height*zoom;
   [base,overlay,$('page-wrap')].forEach(el=>{el.style.width=width+'px';el.style.height=height+'px';});
   $('page-wrap').hidden=false;$('empty').hidden=true;$('page').value=String(pageIndex);
   selected=-1;drag=null;repaint();status(`Page ${pageIndex+1} / ${doc.numPages} · ${items().length} edits`);
  } catch(error){status('PDF render नहीं हुआ: '+error.message);}
  finally{if(token===epoch&&serial===renderSerial){busy=false;controls();}}
 }
 function reset() {
  epoch++;renderSerial++;if(doc)doc.destroy().catch(()=>{});
  doc=null;bytes=null;pages=[];assets.clear();undo=[];redo=[];viewport=null;drag=null;pendingImage=null;selected=-1;pageIndex=0;dirty=false;busy=false;
  base.width=overlay.width=1;base.height=overlay.height=1;
  $('page-wrap').hidden=true;$('empty').hidden=false;$('page').replaceChildren();$('count').textContent='/ 0';
  $('filename').textContent='कोई PDF नहीं चुनी है · अधिकतम 50 MB / 150 pages';$('file').value='';$('image-file').value='';$('text').value='';
  controls();status('Document बंद है। Browser memory से PDF और edits हटा दिए गए हैं।');
 }
 async function openFile(file) {
  if(!file)return;
  if(dirty&&!confirm('Current PDF के unsaved edits छोड़कर नई file खोलें?'))return;
  if(file.size>50*1024*1024){status('PDF 50 MB से छोटी होनी चाहिए।');return;}
  if(!/\.pdf$/i.test(file.name)){status('कृपया PDF file चुनें।');return;}
  if(!window.pdfjsLib||!window.PDFLib){status('PDF libraries नहीं लोड हुईं। Internet चालू करके portal दोबारा खोलें।');return;}
  reset();const token=epoch;busy=true;controls();status('PDF पढ़ी जा रही है…');
  let loaded=null;
  try {
   const source=new Uint8Array(await file.arrayBuffer());
   // Validate before opening; encrypted documents are never opened with ignoreEncryption.
   await PDFLib.PDFDocument.load(source);
   loaded=await pdfjsLib.getDocument({data:source.slice(),isEvalSupported:false,enableScripting:false}).promise;
   if(token!==epoch){await loaded.destroy();return;}
   if(loaded.numPages>150)throw new Error('अधिकतम 150 pages समर्थित हैं।');
   bytes=source;doc=loaded;filename=file.name;pages=Array.from({length:doc.numPages},()=>[]);
   $('filename').textContent=filename;$('count').textContent='/ '+doc.numPages;
   for(let i=0;i<doc.numPages;i++){const opt=document.createElement('option');opt.value=i;opt.textContent=i+1;$('page').append(opt);}
   setTool('select');await renderPage();
  }catch(error){if(loaded&&loaded!==doc)await loaded.destroy();if(token===epoch){reset();status('PDF नहीं खुली। Password-protected / खराब PDF को पहले unlocked copy में save करें। '+error.message);}}
  finally{if(token===epoch){busy=false;controls();}}
 }
 function position(e) {const r=overlay.getBoundingClientRect();return {x:Math.max(0,Math.min(viewport.width,(e.clientX-r.left)/r.width*viewport.width)),y:Math.max(0,Math.min(viewport.height,(e.clientY-r.top)/r.height*viewport.height))};}
 function add(o) {remember();items().push(o);selected=items().length-1;repaint();controls();}
 overlay.addEventListener('pointerdown',e=>{
  if(!doc||busy||!viewport||e.button!==0)return;e.preventDefault();const p=position(e),s=style();
  if(tool==='select'){
   selected=-1;for(let i=items().length-1;i>=0;i--){const o=items()[i];if(p.x>=o.x-4&&p.x<=o.x+o.w+4&&p.y>=o.y-4&&p.y<=o.y+o.h+4){selected=i;break;}}
   if(selected>=0){const o=items()[selected];$('text').value=o.text||'';$('color').value=o.color;$('size').value=o.size;$('pen').value=o.pen;$('bold').checked=o.bold;drag={start:p,original:clone(o),before:clone(pages),moving:true};overlay.setPointerCapture(e.pointerId);}
   repaint();controls();return;
  }
  if(tool==='text'){
   const text=$('text').value;if(!text.trim()){status('पहले sidebar में text लिखें।');$('text').focus();return;}
   const o={type:'text',...s,...p,text};textMetrics(o);add(o);return;
  }
  if(tool==='check'||tool==='cross'){add({type:tool,...s,...p,w:s.size,h:s.size});return;}
  if(tool==='image'){
   if(!pendingImage){status('पहले Image / Signature से image चुनें।');return;}
   const img=assets.get(pendingImage),w=Math.min(150,viewport.width-p.x),h=w*img.height/img.width;
   add({type:'image',...s,...p,asset:pendingImage,w,h});setTool('select');return;
  }
  drag={start:p,points:[p],preview:null};overlay.setPointerCapture(e.pointerId);
 });
 overlay.addEventListener('pointermove',e=>{
  if(!drag||busy)return;const p=position(e);
  if(drag.moving){const o=items()[selected];o.x=Math.max(0,Math.min(viewport.width-o.w,drag.original.x+p.x-drag.start.x));o.y=Math.max(0,Math.min(viewport.height-o.h,drag.original.y+p.y-drag.start.y));}
  else {
   const s=style();let x=Math.min(p.x,drag.start.x),y=Math.min(p.y,drag.start.y),w=Math.abs(p.x-drag.start.x),h=Math.abs(p.y-drag.start.y);
   if(tool==='draw'){
    drag.points.push(p);const xs=drag.points.map(q=>q.x),ys=drag.points.map(q=>q.y);x=Math.min(...xs);y=Math.min(...ys);w=Math.max(1,Math.max(...xs)-x);h=Math.max(1,Math.max(...ys)-y);
    drag.preview={type:'draw',...s,x,y,w,h,points:drag.points.map(q=>[(q.x-x)/w,(q.y-y)/h])};
   }else drag.preview={type:tool,...s,x,y,w,h};
  }repaint();
 });
 function finishDrag(cancel=false){
  if(!drag)return;
  if(drag.moving){if(cancel)pages=drag.before;else if(JSON.stringify(items()[selected])!==JSON.stringify(drag.original)){undo.push(drag.before);if(undo.length>40)undo.shift();redo=[];dirty=true;}}
  else if(!cancel&&drag.preview&&((drag.preview.type==='draw'&&(drag.preview.w>2||drag.preview.h>2))||(drag.preview.w>1&&drag.preview.h>1)))add(drag.preview);
  drag=null;repaint();controls();
 }
 overlay.addEventListener('pointerup',()=>finishDrag());overlay.addEventListener('pointercancel',()=>finishDrag(true));
 root.querySelectorAll('[data-pe-tool]').forEach(b=>b.addEventListener('click',()=>setTool(b.dataset.peTool)));
 $('open').onclick=()=>{$('file').value='';$('file').click();};
 $('file').onchange=()=>openFile($('file').files[0]);
 $('close').onclick=()=>{if(!dirty||confirm('Unsaved edits छोड़कर PDF बंद करें?'))reset();};
 $('image').onclick=()=>{$('image-file').value='';$('image-file').click();};
 $('image-file').onchange=async()=>{
  const file=$('image-file').files[0];if(!file)return;
  if(!['image/png','image/jpeg'].includes(file.type)||file.size>10*1024*1024){status('PNG/JPG image चुनें, अधिकतम 10 MB।');return;}
  const token=epoch,url=URL.createObjectURL(file);busy=true;controls();
  try{const img=new Image();img.src=url;await img.decode();if(token!==epoch)return;if(img.width*img.height>25000000)throw new Error('Image बहुत बड़ी है। पहले resize करें।');pendingImage=nextAsset++;assets.set(pendingImage,img);setTool('image');}
  catch(error){if(token===epoch)status('Image नहीं खुली: '+error.message);}
  finally{URL.revokeObjectURL(url);if(token===epoch){busy=false;controls();}}
 };
 $('apply').onclick=()=>{
  const o=items()[selected];if(!o)return;
  if(o.type==='text'&&!$('text').value.trim()){status('Text खाली नहीं रख सकते; हटाने के लिए Delete selected दबाएँ।');return;}
  remember();Object.assign(o,style());if(o.type==='text'){o.text=$('text').value;textMetrics(o);}repaint();controls();
 };
 function resize(factor){const o=items()[selected];if(!o)return;remember();if(o.type==='text'){o.size=Math.max(6,Math.min(120,o.size*factor));textMetrics(o);$('size').value=Math.round(o.size);}else{o.w=Math.max(3,Math.min(viewport.width,o.w*factor));o.h=Math.max(3,Math.min(viewport.height,o.h*factor));}repaint();controls();}
 $('smaller').onclick=()=>resize(.9);$('larger').onclick=()=>resize(1.1);
 $('delete').onclick=()=>{if(selected<0)return;remember();items().splice(selected,1);selected=-1;repaint();controls();};
 function travel(from,to){if(!from.length||busy)return;to.push(clone(pages));pages=from.pop();selected=-1;dirty=true;repaint();controls();}
 $('undo').onclick=()=>travel(undo,redo);$('redo').onclick=()=>travel(redo,undo);
 $('prev').onclick=()=>{if(pageIndex>0){pageIndex--;renderPage();}};
 $('next').onclick=()=>{if(pageIndex<doc.numPages-1){pageIndex++;renderPage();}};
 $('page').onchange=()=>{pageIndex=Number($('page').value);renderPage();};$('zoom').onchange=renderPage;
 root.addEventListener('keydown',e=>{
  if(!doc||busy||['INPUT','TEXTAREA','SELECT'].includes(e.target.tagName))return;
  if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='z'){e.preventDefault();e.shiftKey?travel(redo,undo):travel(undo,redo);}
  else if(e.key==='Delete'&&selected>=0){e.preventDefault();$('delete').click();}
  else if(e.key==='Escape'){finishDrag(true);setTool('select');}
 });
 $('download').onclick=async()=>{
  if(!doc||busy)return;const token=epoch;busy=true;controls();status('PDF तैयार हो रही है…');
  try{
   const output=await PDFLib.PDFDocument.load(bytes);
   for(let i=0;i<pages.length;i++){
    if(token!==epoch)return;if(!pages[i].length)continue;
    status(`Edits save हो रहे हैं: page ${i+1} / ${pages.length}`);
    const sourcePage=await doc.getPage(i+1),view=sourcePage.getViewport({scale:1});
    const scale=Math.min(2,3500/Math.max(view.width,view.height));
    const canvas=document.createElement('canvas');canvas.width=Math.ceil(view.width*scale);canvas.height=Math.ceil(view.height*scale);
    const ctx=canvas.getContext('2d');ctx.scale(canvas.width/view.width,canvas.height/view.height);pages[i].forEach(o=>drawItem(ctx,o));
    const png=await output.embedPng(canvas.toDataURL('image/png'));
    const origin=view.convertToPdfPoint(0,view.height);
    // Map the displayed crop-box back into PDF coordinates, including /Rotate and /UserUnit.
    const unit=Math.hypot(view.transform[0],view.transform[1]);
    output.getPage(i).drawImage(png,{x:origin[0],y:origin[1],width:view.width/unit,height:view.height/unit,rotate:PDFLib.degrees(((sourcePage.rotate%360)+360)%360)});
    canvas.width=canvas.height=1;
   }
   const data=await output.save();if(token!==epoch)return;
   const blob=new Blob([data],{type:'application/pdf'}),url=URL.createObjectURL(blob),link=document.createElement('a');
   link.href=url;link.download=filename.replace(/\.pdf$/i,'')+'-edited.pdf';document.body.append(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),60000);
   dirty=false;status('PDF download तैयार है। Original file नहीं बदली। Whiteout के नीचे मूल content रहता है।');
  }catch(error){if(token===epoch)status('Download नहीं हो सकी: '+error.message);}
  finally{if(token===epoch){busy=false;controls();}}
 };
 window.addEventListener('beforeunload',e=>{if(dirty){e.preventDefault();e.returnValue='';}});
 window.addEventListener('portal-auth-cleared',reset);
 controls();
})();

</script>
</body>
</html>
