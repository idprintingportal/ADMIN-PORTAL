/* ID Card Portal — Google Apps Script backend
 * Paste this entire file into Extensions > Apps Script for the Google Sheet.
 * Deploy it as a Web App, then keep its /exec URL in GOOGLE_SCRIPT_URL in the HTML.
 */

const DISTRIBUTORS_SHEET_NAME = 'Distributors';
// Explicitly bind the web app to the production data sheet.
const PORTAL_SPREADSHEET_ID = '1zrz_vX1NkFeVPa7fbQA36U1Mx05vEPtkVKbT5BUbBCA';
const IMGBB_UPLOAD_URL = 'https://api.imgbb.com/1/upload';
const HEADERS = [
  'id', 'name', 'email', 'pass', 'assignedTimestamp', 'expiryTime',
  'adminMessage', 'adminImage', 'status', 'paymentStatus', 'paymentPlan',
  'paymentAmount', 'paymentTxnId', 'paymentScreenshot', 'approvalGranted',
  'approved', 'accessApproved', 'approvalNote', 'screenshotStatus',
  'distributorMessage', 'distributorReplyImage', 'distributorReplyAt',
  'renewalRequested', 'renewalPlan', 'renewalAmount', 'renewalTxnId',
  'renewalScreenshot', 'renewalRequestedAt', 'passwordHash', 'paymentApprovedAt',
  'pdfPremiumStatus','pdfPremiumAmount','pdfPremiumTxnId','pdfPremiumScreenshot','pdfPremiumRequestId','pdfPremiumRequestedAt','pdfPremiumApprovedAt','pdfPremiumExpiry','paymentRequestId','paymentRequestedAt',
  'premiumBundleStatus','premiumBundleExpiry','validityPlan','officeName','mobile'
];


// Server-side authentication. All state-changing actions use authenticated POST.
const AUTH_ITERATIONS = 600000;
const SESSION_SECONDS = 3600;
const MAX_IMAGE_CHARS = 7000000;

function securityProperties_() { return PropertiesService.getScriptProperties(); }
function securityReady_() {
  const p = securityProperties_();
  if (!p.getProperty('ADMIN_EMAIL') || !p.getProperty('ADMIN_PASSWORD_HASH') || !p.getProperty('AUTH_PEPPER')) throw new Error('Security setup required. Contact admin.');
}
function withLock_(fn) {
  const lock = LockService.getScriptLock(); lock.waitLock(30000);
  try { return fn(); } finally { lock.releaseLock(); }
}
function randomToken_() { return Utilities.getUuid().replace(/-/g, '') + Utilities.getUuid().replace(/-/g, ''); }
function sha256_(text) { return PortalHash.sha256().update(String(text)).digest('hex'); }
function equalSecret_(a, b) {
  a = String(a || ''); b = String(b || '');
  let diff = a.length ^ b.length;
  for (let i = 0; i < Math.max(a.length, b.length); i++) diff |= (a.charCodeAt(i) || 0) ^ (b.charCodeAt(i) || 0);
  return diff === 0;
}
function pbkdf2_(password, salt, rounds) {
  const key = PortalHash.utils.toArray(password);
  let u = PortalHash.hmac(PortalHash.sha256, key).update(PortalHash.utils.toArray(salt).concat([0, 0, 0, 1])).digest();
  const result = u.slice();
  for (let i = 1; i < rounds; i++) {
    u = PortalHash.hmac(PortalHash.sha256, key).update(u).digest();
    for (let j = 0; j < 32; j++) result[j] ^= u[j];
  }
  return PortalHash.utils.toHex(result);
}
function hashPassword_(password) {
  const salt = randomToken_();
  const pepper = securityProperties_().getProperty('AUTH_PEPPER');
  if (!pepper) throw new Error('Security setup required.');
  const keyed = PortalHash.hmac(PortalHash.sha256, pepper).update(password).digest('hex');
  return ['pbkdf2-sha256', AUTH_ITERATIONS, salt, pbkdf2_(keyed, salt, AUTH_ITERATIONS)].join('$');
}
function verifyPassword_(password, encoded) {
  const parts = String(encoded || '').split('$');
  if (parts.length !== 4 || parts[0] !== 'pbkdf2-sha256' || Number(parts[1]) !== AUTH_ITERATIONS) return false;
  const keyed = PortalHash.hmac(PortalHash.sha256, securityProperties_().getProperty('AUTH_PEPPER')).update(password).digest('hex');
  return equalSecret_(pbkdf2_(keyed, parts[2], AUTH_ITERATIONS), parts[3]);
}
function email_(value){
  const email=String(value||'').trim().toLowerCase();if(email.length>254||email.includes('..'))throw new Error('Valid email required.');const parts=email.split('@');if(parts.length!==2||!parts[0]||parts[0].length>64||parts[0][0]==='.'||parts[0].slice(-1)==='.')throw new Error('Valid email required.');
  if(!/^[a-z0-9.!#$%&'*+\/=?^_\`{|}~-]+$/i.test(parts[0])||parts[1].length>253||!parts[1].includes('.')||parts[1].split('.').some(x=>!x||x.length>63||!/^([a-z0-9](?:[a-z0-9-]*[a-z0-9])?)$/i.test(x)))throw new Error('Valid email required.');return email;
}
function text_(value,max){
  const result=String(value==null?'':value).normalize('NFC').trim();if(result.length>max)throw new Error('Text is too long.');if(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/.test(result))throw new Error('Invalid text.');return result;
}
function newPassword_(value) {
  const password = String(value || '');
  if (password.length < 12 || password.length > 128) throw new Error('Use a password with 12–128 characters.');
  return password;
}
function record_(email){
  const matches=getDistributors_().filter(d=>String(d.email).trim().toLowerCase()===email);if(matches.length>1)throw new Error('Duplicate account rows found. Contact admin.');return matches[0]||null;
}
function publicRecord_(record) {
  const result = {};
  HEADERS.forEach(key => { if (!['pass', 'passwordHash'].includes(key) && record[key] !== undefined) result[key] = record[key]; });
  return result;
}
function expiry_(record) {
  if (record.expiryTime !== '' && record.expiryTime !== undefined && record.expiryTime !== null) return Number(record.expiryTime);
  const assigned = Number(record.assignedTimestamp);
  const plan = renewalPlan_(record.paymentPlan || '1 Month');
  return assigned > 0 && plan ? assigned + plan.days * 86400000 : 0;
}
function stateText_(value) { return String(value == null ? '' : value).trim().toLowerCase(); }
function hasApproval_(record) {
  return [record.approved, record.approvalGranted, record.accessApproved].some(v => stateText_(v) === 'true');
}
function accessState_(record) {
  record = Object.assign({}, record);
  ['status','paymentStatus','renewalRequested','approved','approvalGranted','accessApproved'].forEach(key => record[key] = stateText_(record[key]));
  if (String(record.status).toLowerCase() === 'stopped') return 'stopped';
  if (String(record.renewalRequested).toLowerCase() === 'true') return 'renewal_pending';
  if (record.renewalRequestedAt && String(record.paymentStatus).toLowerCase() === 'rejected') return 'renewal';
  if (String(record.paymentStatus).toLowerCase() === 'pending') return 'pending';
  if (String(record.paymentStatus).toLowerCase() === 'rejected') return 'rejected';
  const approved = [record.approved, record.approvalGranted, record.accessApproved].some(v => String(v).toLowerCase() === 'true');
  if (!approved || String(record.status).toLowerCase() !== 'active' || String(record.paymentStatus).toLowerCase() !== 'approved') return 'pending';
  return expiry_(record) > Date.now() ? 'active' : 'renewal';
}
function throttle_(bucket,limit,seconds){
  return withLock_(()=>{
    const now=Date.now(),windowMs=seconds*1000,key=sha256_('rate|'+bucket),s=rateLedger_(),all=rows_(s,4),i=all.findIndex(r=>r[0]===key);
    let start=i<0?now:Number(all[i][1]),count=i<0?0:Number(all[i][2]);if(!start||now-start>=windowMs){start=now;count=0;}
    if(count>=limit)throw new Error('Too many attempts. Please try later.');count++;
    if(i<0)s.appendRow([key,start,count,now]);else s.getRange(i+2,2,1,3).setValues([[start,count,now]]);
    CacheService.getScriptCache().put('limit:'+key,String(count),Math.min(21600,seconds));
  });
}
function authenticatePassword_(email, password) {
  securityReady_();
  throttle_('login-global', 100, 900);
  throttle_('login:' + email, 10, 900);
  if (!password || password.length > 128) throw new Error('Invalid email or password.');
  const p = securityProperties_();
  const admin = email === p.getProperty('ADMIN_EMAIL').trim().toLowerCase();
  const record = admin ? null : record_(email);
  const hash = admin ? p.getProperty('ADMIN_PASSWORD_HASH') : record && record.passwordHash;
  // Unknown accounts do the same expensive verification; legacy plaintext is never accepted online.
  const valid = verifyPassword_(password, hash || p.getProperty('ADMIN_PASSWORD_HASH'));
  if (!hash || !valid) throw new Error('Invalid email or password.');
  if (!admin && maintenanceActive_()) throw new Error(maintenanceMessage_());
  return { email, role: admin ? 'admin' : 'distributor', version: sha256_(hash), record };
}
function issueSession_(principal){
  const token=randomToken_(),tokenHash=sha256_(token),expires=Date.now()+SESSION_SECONDS*1000,saved={email:principal.email,role:principal.role,version:principal.version,expires,panelUntil:0};
  withLock_(()=>{sessionLedger_().appendRow([tokenHash,saved.email,saved.role,saved.version,expires,0,0,Date.now()]);SpreadsheetApp.flush();});
  CacheService.getScriptCache().put('session:'+tokenHash,JSON.stringify(saved),SESSION_SECONDS);
  return {success:true,token,expires,role:principal.role,state:principal.role==='admin'?'active':accessState_(principal.record),record:principal.record?publicRecord_(principal.record):null};
}
function session_(data){
  securityReady_();const token=String(data.token||'');if(!/^[a-f0-9]{64}$/i.test(token))throw new Error('Login required.');
  const tokenHash=sha256_(token),cache=CacheService.getScriptCache();let raw=cache.get('session:'+tokenHash),principal=raw?JSON.parse(raw):null;
  if(!principal){const row=rows_(sessionLedger_(),8).find(r=>r[0]===tokenHash&&!Number(r[6]));if(row)principal={email:row[1],role:row[2],version:row[3],expires:Number(row[4]),panelUntil:Number(row[5])||0};}
  if(!principal||principal.expires<=Date.now())throw new Error('Session expired. Please login again.');
  const p=securityProperties_();if(principal.role==='admin'){
    if(principal.email!==p.getProperty('ADMIN_EMAIL').trim().toLowerCase()||principal.version!==sha256_(p.getProperty('ADMIN_PASSWORD_HASH')))throw new Error('Session expired. Please login again.');
  }else{principal.record=record_(principal.email);if(!principal.record||principal.version!==sha256_(principal.record.passwordHash))throw new Error('Session expired. Please login again.');if(maintenanceActive_())throw new Error(maintenanceMessage_());}
  cache.put('session:'+tokenHash,JSON.stringify(principal),Math.max(1,Math.ceil((principal.expires-Date.now())/1000)));return principal;
}
function admin_(principal) {
  if (principal.role !== 'admin') throw new Error('Admin access required.');
  if (!(Number(principal.panelUntil) > Date.now())) throw new Error('Admin panel is locked. Enter your admin password to unlock it.');
}
function unlockAdminPanel_(data,principal){
  if(principal.role!=='admin')throw new Error('Admin access required.');throttle_('panel-unlock:'+principal.email,10,300);
  const password=String(data.password||'');if(!password||password.length>128||!verifyPassword_(password,securityProperties_().getProperty('ADMIN_PASSWORD_HASH')))throw new Error('Incorrect admin password.');
  return withLock_(()=>{const current=session_(data);if(current.role!=='admin'||current.version!==principal.version)throw new Error('Session changed. Please login again.');current.panelUntil=Math.min(current.expires,Date.now()+300000);
    const hash=sha256_(data.token);updateSessionLedger_(hash,{panelUntil:current.panelUntil});CacheService.getScriptCache().put('session:'+hash,JSON.stringify(current),Math.max(1,Math.ceil((current.expires-Date.now())/1000)));return {success:true,panelUntil:current.panelUntil};});
}
function lockAdminPanel_(data,principal){
  if(principal.role!=='admin')throw new Error('Admin access required.');return withLock_(()=>{const current=session_(data);current.panelUntil=0;const hash=sha256_(data.token);updateSessionLedger_(hash,{panelUntil:0});CacheService.getScriptCache().put('session:'+hash,JSON.stringify(current),Math.max(1,Math.ceil((current.expires-Date.now())/1000)));return {success:true};});
}
function own_(principal, data) {
  if (principal.role !== 'distributor' || (data.email && email_(data.email) !== principal.email)) throw new Error('You can only update your own account.');
  data.email = principal.email;
}
function validImage_(value) {
  const data = String(value || '');
  const match = data.match(/^data:image\/(png|jpeg|webp);base64,([A-Za-z0-9+/]+={0,2})$/);
  if (!match || data.length > MAX_IMAGE_CHARS) throw new Error('Use a JPG, PNG or WEBP image under 5 MB.');
  const bytes = Utilities.base64Decode(match[2]).map(v => v & 255);
  const valid = match[1] === 'png' ? bytes.slice(0,8).join(',') === '137,80,78,71,13,10,26,10'
    : match[1] === 'jpeg' ? bytes[0] === 255 && bytes[1] === 216 && bytes[2] === 255
    : String.fromCharCode.apply(null,bytes.slice(0,4)) === 'RIFF' && String.fromCharCode.apply(null,bytes.slice(8,12)) === 'WEBP';
  if (!valid) throw new Error('Image file content does not match its type.');
  return data;
}
function doGet(e) {
  if (e && e.parameter && e.parameter.action === 'health') return json_({ success: true, version: 'security-reviewed-v2' });
  return json_({ success: false, error: 'Use authenticated POST. Public record access and GET mutations are disabled.' });
}
function doPost(e) {
  try {
    const body = e && e.postData && e.postData.contents;
    if (!body || body.length > MAX_IMAGE_CHARS + 20000) throw new Error('Invalid request size.');
    const data = JSON.parse(body);
    if (!data || Array.isArray(data) || typeof data !== 'object') throw new Error('Invalid request.');
    securityReady_();
    if (data.action === 'login') return json_(issueSession_(authenticatePassword_(email_(data.email), String(data.password || ''))));
    if (data.action === 'requestPasswordReset') return json_(requestPasswordReset_(data));
    if (data.action === 'verifyPasswordOtp') return json_(verifyPasswordOtp_(data));
    if (data.action === 'resetPassword') return json_(resetPassword_(data));
    if (data.action === 'requestRegistrationOtp') return json_(requestRegistrationOtp_(data));
    if (data.action === 'verifyRegistrationOtp') return json_(verifyRegistrationOtp_(data));
    if (data.action === 'register') return json_(registerSecure_(data, false));
    if (data.action === 'updatePassword') return json_(changePasswordSecure_(data));
    const principal = session_(data);
    if(data.action==='authorizePdfDownload')return json_(authorizePdfDownload_(data));
    if(data.action==='getManagedImage')return json_(managedImage_(data,principal));
    if(data.action==='getPdfPremium')return json_(premiumInfo_(principal));
    if(data.action==='reviewPdfPremium')return json_(reviewPremium_(data));
    if(data.action==='submitPdfPremium'){own_(principal,data);throttle_('premium:'+principal.email,10,900);return json_(submitPremium_(data));}
    if (data.action === 'unlockAdminPanel') return json_(unlockAdminPanel_(data, principal));
    if (data.action === 'lockAdminPanel') return json_(lockAdminPanel_(data, principal));
    if (data.action === 'logout') {
      const sessionHash=sha256_(data.token);CacheService.getScriptCache().remove('session:'+sessionHash);withLock_(()=>updateSessionLedger_(sessionHash,{revokedAt:Date.now()}));
      return json_({success:true});
    }
    if (data.action === 'getMe') return json_({success:true, role:principal.role, state:principal.role === 'admin' ? 'active' : accessState_(principal.record), record:principal.record ? publicRecord_(principal.record) : null, maintenance:maintenanceSettings_()});
    if (data.action === 'getMaintenance') return json_({success:true,maintenance:maintenanceSettings_()});
    if (data.action === 'setMaintenance') return json_(setMaintenance_(data,principal));
    if (data.action === 'getDistributors') {
      admin_(principal); return json_({success:true, records:getDistributors_().map(publicRecord_)});
    }
    if (['addDistributor','deleteDistributor','toggleStatus','messageDistributor','reviewDistributorPayment'].includes(data.action)) {
      admin_(principal);
      if (data.action === 'addDistributor') return json_(registerSecure_(data, true));
      if (data.action === 'deleteDistributor') return json_(withLock_(() => deleteDistributor_(String(data.id))));
      if (data.action === 'reviewDistributorPayment') return json_(reviewPayment_(data));
      const email = email_(data.email);
      if (data.action === 'toggleStatus') {
        if (!['Active','Stopped'].includes(data.status)) throw new Error('Invalid status.');
        return json_(withLock_(() => {
          const record = record_(email);
          if (!record) throw new Error('Distributor not found.');
          if (data.status === 'Active' && (stateText_(record.paymentStatus) !== 'approved' || !hasApproval_(record) || !(expiry_(record) > Date.now()) || stateText_(record.renewalRequested) === 'true')) throw new Error('Payment approval, approval flags and valid plan required. Contact admin for access diagnosis.');
          return updateDistributor_(email, {status:data.status});
        }));
      }
      const message = text_(data.message, 3000);
      let imageUrl = '';
      if (data.imageUrl) {
        const image = validImage_(data.imageUrl);
        const uploaded = {success:true,url:storePortalImage_(image,email,'general')};
        if (!uploaded.success) throw new Error('Image upload failed. Check ImgBB configuration.');
        imageUrl = uploaded.url;
      }
      return json_(updateAdminMessage_(email,message,imageUrl));
    }
    own_(principal, data);
    throttle_('write:' + principal.email, 30, 900);
    const state = accessState_(principal.record);
    if (data.action === 'submitRenewal') {
      if (state !== 'renewal') throw new Error('Renewal is not available or is already pending.');
      data.imageData = validImage_(data.imageData);
      data.renewalTxnId = text_(data.renewalTxnId, 150);
      return json_(submitRenewal_(data));
    }
    if (data.action === 'uploadPaymentScreenshot' || data.action === 'uploadScreenshot') {
      if (!['pending','rejected'].includes(state)) throw new Error('Signup screenshot cannot be changed for this account.');
      data.imageData = validImage_(data.imageData);
      return json_(uploadPaymentScreenshot_(data));
    }
    if (data.action === 'replyToAdmin') {
      if (state !== 'active') throw new Error('An active approved account is required.');
      data.message = text_(data.message, 3000);
      if (data.imageData) data.imageData = validImage_(data.imageData);
      return json_(replyToAdmin_(data));
    }
    throw new Error('Unknown action.');
  } catch (error) {
    // Do not echo payloads, passwords, tokens or external-service responses.
    return json_({success:false,error:safeError_(error)});
  }
}
function registerSecure_(data,adminCreated){
  const email=email_(data.email),name=text_(data.name,100),officeName=text_(data.officeName,150),mobile=text_(data.mobile,20),password=newPassword_(data.pass),plan=renewalPlan_(data.paymentPlan||(adminCreated?'1 Month':''));
  if(!officeName||!/^\+?[0-9][0-9 ()-]{7,18}$/.test(mobile))throw new Error('Office/center name and valid mobile number required.');
  if(!name||!plan||email===securityProperties_().getProperty('ADMIN_EMAIL').trim().toLowerCase())throw new Error('Invalid registration.');
  if(!adminCreated){const otpRaw=securityProperties_().getProperty(registrationOtpKey_(email)),otpEntry=otpRaw?JSON.parse(otpRaw):null;if(!otpEntry||!otpEntry.verified||otpEntry.expires<Date.now()||sha256_('registration-verified|'+String(data.registrationToken||''))!==otpEntry.verifyHash)throw new Error('Email OTP verification required.');}
  if(!adminCreated){throttle_('signup-global',20,3600);throttle_('signup:'+email,3,3600);}
  const txn=adminCreated?'Admin Assignment':text_(data.paymentTxnId,150),requestId=randomToken_();if(!txn)throw new Error('Payment transaction ID required.');
  const hash=hashPassword_(password),record=withLock_(()=>{
    const sheet=getSheet_();if(findDistributorRow_(sheet,email))throw new Error('Account already exists. Login to continue or contact admin.');if(!adminCreated)claimTransaction_(txn,email,'membership',requestId);
    const now=Date.now(),map=getHeaderMap_(sheet),row=new Array(sheet.getLastColumn()).fill(''),record={id:randomToken_(),name,email,officeName,mobile,pass:'',passwordHash:hash,assignedTimestamp:now,expiryTime:adminCreated?now+plan.days*86400000:0,validityPlan:plan.label,status:adminCreated?'Active':'Pending',paymentStatus:adminCreated?'Approved':'Pending',paymentPlan:plan.label,paymentAmount:plan.amount,paymentTxnId:txn,paymentRequestId:requestId,paymentRequestedAt:now,approved:adminCreated,approvalGranted:adminCreated,accessApproved:adminCreated,approvalNote:adminCreated?'Admin assignment':'Awaiting screenshot and admin approval'};
    try{Object.keys(record).forEach(k=>{row[map[k.toLowerCase()]-1]=sheetValue_(record[k]);});sheet.appendRow(row);SpreadsheetApp.flush();}catch(e){if(!adminCreated)releaseTransaction_(email,'membership',requestId);throw e;}return record;
  });return adminCreated?{success:true}:issueSession_({email,role:'distributor',version:sha256_(hash),record});
}
function changePasswordSecure_(data) {
  const email=email_(data.email), password=newPassword_(data.newPass);
  const principal=authenticatePassword_(email,String(data.oldPass || ''));
  const newHash=hashPassword_(password);
  return withLock_(() => {
    const currentHash=principal.role==='admin'?securityProperties_().getProperty('ADMIN_PASSWORD_HASH'):record_(email).passwordHash;
    if (sha256_(currentHash)!==principal.version) throw new Error('Account changed. Please login again.');
    if(principal.role==='admin') securityProperties_().setProperty('ADMIN_PASSWORD_HASH',newHash);
    else updateDistributor_(email,{passwordHash:newHash,pass:''});
    return {success:true};
  });
}
function sheetValue_(value) {
  // Google Sheets treats a leading equals sign as a formula; guard all user text.
  return typeof value === 'string' && /^[\s]*[=+@-]/.test(value) ? "'" + value : value;
}

// Run manually in the editor before deployment. No network action can call setup/migration.
function setupSecurity() {
  return withLock_(() => {
    const p=securityProperties_();
    const email=email_(p.getProperty('ADMIN_EMAIL'));
    p.setProperty('ADMIN_EMAIL',email);
    if(!p.getProperty('AUTH_PEPPER') && p.getProperty('ADMIN_PASSWORD_HASH')) throw new Error('AUTH_PEPPER is missing. Restore it from a secure backup; do not regenerate it.');
    if(!p.getProperty('AUTH_PEPPER')) p.setProperty('AUTH_PEPPER',randomToken_());
    if(!p.getProperty('ADMIN_PASSWORD_HASH')) {
      const password=newPassword_(p.getProperty('ADMIN_SETUP_PASSWORD'));
      p.setProperty('ADMIN_PASSWORD_HASH',hashPassword_(password));
    }
    p.deleteProperty('ADMIN_SETUP_PASSWORD');
    p.deleteProperty('ADMIN_REVIEW_KEY');
    getSheet_();
    console.log('Admin security initialized. Run migratePasswords until remaining is zero.');
  });
}
function migratePasswords() {
  securityReady_();
  return withLock_(() => {
    const pending=getDistributors_().filter(d=>String(d.pass || '') || !d.passwordHash);
    let migrated=0,needsReset=pending.filter(d=>!d.passwordHash && !String(d.pass || '').trim()).length;
    pending.filter(d=>d.passwordHash || String(d.pass || '').trim()).slice(0,3).forEach(record=>{
      const legacy=String(record.pass || '').trim();
      if(!record.passwordHash && !legacy) { needsReset++; return; }
      const changes={pass:'',passwordHash:record.passwordHash || hashPassword_(legacy)};
      // Preserve approved legacy accounts whose old code stored only paymentStatus/status.
      if(String(record.paymentStatus).toLowerCase()==='approved' && ['active','stopped'].includes(String(record.status).toLowerCase())) {
        changes.approved=true;changes.approvalGranted=true;changes.accessApproved=true;
      }
      if(!record.expiryTime && record.paymentStatus==='Approved') changes.expiryTime=expiry_(record);
      updateDistributor_(record.email,changes);migrated++;
    });
    const remaining=getDistributors_().filter(d=>String(d.pass || '') || !d.passwordHash).length;
    console.log(JSON.stringify({migrated,remaining,needsReset}));
    return {migrated,remaining,needsReset};
  });
}

// Owner-only recovery in the Apps Script editor. Not exposed by doPost.
function resetDistributorPassword() {
  securityReady_();
  return withLock_(() => {
    const p=securityProperties_(),rawEmail=String(p.getProperty('RESET_DISTRIBUTOR_EMAIL')||''),rawPassword=String(p.getProperty('RESET_DISTRIBUTOR_PASSWORD')||'');
    if(!rawEmail||!rawPassword) throw new Error('Set RESET_DISTRIBUTOR_EMAIL and RESET_DISTRIBUTOR_PASSWORD in Script Properties before running this owner-only recovery.');
    const email=email_(rawEmail);
    if(!record_(email)) throw new Error('Distributor not found.');
    const hash=hashPassword_(newPassword_(rawPassword)),result=updateDistributor_(email,{passwordHash:hash,pass:''});
    if(!result.success) throw new Error(result.error||'Password reset could not be saved.');
    p.deleteProperty('RESET_DISTRIBUTOR_EMAIL');p.deleteProperty('RESET_DISTRIBUTOR_PASSWORD');
    revokeSessionsForEmail_(email);
    console.log('Distributor password reset. Previous sessions are invalid.');
  });
}

// Editor-only diagnostics and narrowly scoped legacy repair; never dispatched by doPost.
// Set ACCESS_CHECK_EMAIL in Script Properties. Do not put passwords in this property.
function accessCheckRecord_() {
  securityReady_();
  const rawEmail=String(securityProperties_().getProperty('ACCESS_CHECK_EMAIL')||'');
  if(!rawEmail) throw new Error('Set ACCESS_CHECK_EMAIL to an existing distributor email in Script Properties before running this diagnostic.');
  const email = email_(rawEmail);
  const matches = getDistributors_().filter(d => stateText_(d.email) === email);
  if (matches.length !== 1) throw new Error('Expected exactly one matching account. Check missing or duplicate email rows.');
  return matches[0];
}
function diagnoseDistributorAccess() {
  const record = accessCheckRecord_();
  const report = {
    state: accessState_(record), status: stateText_(record.status),
    paymentStatus: stateText_(record.paymentStatus), hasApproval: hasApproval_(record),
    renewalRequested: stateText_(record.renewalRequested),
    validExpiry: Number.isFinite(expiry_(record)) && expiry_(record) > Date.now(),
    hasPasswordHash: Boolean(record.passwordHash),
    legacyRepairEligible: legacyRepairEligible_(record)
  };
  console.log(JSON.stringify(report));
  return report;
}
function legacyRepairEligible_(record) {
  return stateText_(record.status) === 'active' && stateText_(record.paymentStatus) === 'approved' &&
    ['', 'false'].includes(stateText_(record.renewalRequested)) &&
    Number.isFinite(expiry_(record)) && expiry_(record) > Date.now() && !hasApproval_(record);
}
function repairLegacyDistributorAccess() {
  return withLock_(() => {
    const p = securityProperties_();
    const record = accessCheckRecord_();
    // Owner explicitly confirms this one account; no bulk or automatic approval.
    if (p.getProperty('ACCESS_REPAIR_CONFIRM') !== 'CONFIRM_EXISTING_APPROVAL') throw new Error('Verify existing payment approval, then set ACCESS_REPAIR_CONFIRM to CONFIRM_EXISTING_APPROVAL.');
    if (!legacyRepairEligible_(record)) throw new Error('Not eligible: requires Active, Approved, valid expiry, no renewal and missing approval flags. No changes made.');
    const result = updateDistributor_(record.email, {
      approved:true, approvalGranted:true, accessApproved:true,
      approvalNote:'Owner confirmed existing approval; legacy flags repaired at ' + new Date().toISOString()
    });
    if (!result.success) throw new Error(result.error);
    p.deleteProperty('ACCESS_REPAIR_CONFIRM');
    // No change to expiry, password, payment evidence or stopped/pending accounts.
    return diagnoseDistributorAccess();
  });
}



function getSheet_() {
  const spreadsheet = SpreadsheetApp.openById(PORTAL_SPREADSHEET_ID);
  let sheet = spreadsheet.getSheetByName(DISTRIBUTORS_SHEET_NAME);
  if (!sheet) sheet = spreadsheet.insertSheet(DISTRIBUTORS_SHEET_NAME);
  ensureHeaders_(sheet);
  return sheet;
}

function ensureHeaders_(sheet) {
  const current = sheet.getLastColumn() ? sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0] : [];
  const lower = current.map(value => String(value).trim().toLowerCase());
  HEADERS.forEach(header => {
    if (!lower.includes(header.toLowerCase())) {
      sheet.getRange(1, sheet.getLastColumn() + 1).setValue(header);
      lower.push(header.toLowerCase());
    }
  });
}

function getHeaderMap_(sheet) {
  const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  return headers.reduce((map, header, index) => {
    map[String(header).trim().toLowerCase()] = index + 1;
    return map;
  }, {});
}

function getDistributors_() {
  const sheet = getSheet_();
  const lastRow = sheet.getLastRow();
  if (lastRow < 2) return [];
  const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  const emailIndex = headers.findIndex(header => String(header).trim().toLowerCase() === 'email');
  return sheet.getRange(2, 1, lastRow - 1, headers.length).getValues()
    .filter(row => emailIndex >= 0 && String(row[emailIndex] || '').trim() !== '')
    .map(row => headers.reduce((record, header, index) => {
      const canonical = HEADERS.find(key => key.toLowerCase() === String(header).trim().toLowerCase());
      if (canonical) record[canonical] = row[index];
      return record;
    }, {}));
}

function findDistributorRow_(sheet, email) {
  const emailColumn = getHeaderMap_(sheet).email;
  if (!emailColumn) return 0;
  const wanted = String(email || '').trim().toLowerCase();
  const lastRow = sheet.getLastRow();
  if (lastRow < 2) return 0;
  const emails = sheet.getRange(2, emailColumn, lastRow - 1, 1).getValues();
  const index = emails.findIndex(row => String(row[0] || '').trim().toLowerCase() === wanted);
  return index < 0 ? 0 : index + 2;
}

function updateDistributor_(email,changes){
  const sheet=getSheet_(),row=findDistributorRow_(sheet,email);if(!row)return {success:false,error:'Distributor not found.'};const map=getHeaderMap_(sheet),values=sheet.getRange(row,1,1,sheet.getLastColumn()).getValues()[0];
  Object.keys(changes).forEach(key=>{const column=map[key.toLowerCase()];if(column&&changes[key]!==undefined)values[column-1]=sheetValue_(changes[key]);});sheet.getRange(row,1,1,values.length).setValues([values]);SpreadsheetApp.flush();return {success:true};
}

function deleteDistributor_(id){
  const sheet=getSheet_(),idColumn=getHeaderMap_(sheet).id,lastRow=sheet.getLastRow();if(lastRow<2||!idColumn)return {success:false,error:'Distributor not found.'};const ids=sheet.getRange(2,idColumn,lastRow-1,1).getValues(),index=ids.findIndex(r=>String(r[0])===String(id));if(index<0)return {success:false,error:'Distributor not found.'};
  const record=getDistributors_().find(d=>String(d.id)===String(id));if(record)scheduleImageRetention_(IMAGE_FIELDS_.map(k=>record[k]),Date.now()+RETENTION_MS_);sheet.deleteRow(index+2);return {success:true};
}

function uploadPaymentScreenshot_(data){
  const email=email_(data.email),imageData=validImage_(data.imageData||data.paymentScreenshot||data.screenshotUrl),ref=storePortalImage_(imageData,email,'payment');
  try{return withLock_(()=>{const current=record_(email);if(!current||!['pending','rejected'].includes(stateText_(current.paymentStatus))||!['pending','rejected'].includes(accessState_(current)))throw new Error('Account changed or payment is already approved. Login again; approval was not changed.');
    const oldRef=String(current.paymentScreenshot||''),requestId=randomToken_(),result=updateDistributor_(email,{paymentScreenshot:ref,screenshotStatus:'Uploaded',status:'Pending',paymentStatus:'Pending',approved:false,approvalGranted:false,accessApproved:false,paymentRequestId:requestId,paymentRequestedAt:Date.now()});if(!result.success)throw new Error(result.error);
    try{rebindTransaction_(current.paymentTxnId,email,requestId);if(oldRef&&oldRef!==ref)discardManagedImage_(oldRef);}catch(ignore){console.log('Previous screenshot cleanup will retry during scheduled cleanup.');}return {success:true,screenshotUrl:ref,requestId,replaced:Boolean(oldRef)};});
  }catch(e){discardManagedImage_(ref);throw e;}
}

function replyToAdmin_(data){
  const email=email_(data.email),message=text_(data.message,3000);if(!message&&!data.imageData)throw new Error('Reply text or image is required.');const ref=data.imageData?storePortalImage_(validImage_(data.imageData),email,'general'):'';
  try{return withLock_(()=>{const current=record_(email);if(!current||accessState_(current)!=='active')throw new Error('An active approved account is required.');const changes={distributorMessage:message,distributorReplyAt:Date.now()};if(ref)changes.distributorReplyImage=ref;const result=updateDistributor_(email,changes);if(!result.success)throw new Error(result.error);return result;});}catch(e){if(ref)discardManagedImage_(ref);throw e;}
}

function submitRenewal_(data) {
  const lock = LockService.getScriptLock();
  lock.waitLock(30000);
  try { return submitRenewalLocked_(data); } finally { lock.releaseLock(); }
}

function submitRenewalLocked_(data){
  const email=email_(data.email),selectedPlan=renewalPlan_(data.renewalPlan),txn=text_(data.renewalTxnId,150);if(!selectedPlan||!txn)throw new Error('Renewal plan, transaction ID, and screenshot are required.');validImage_(data.imageData);
  const current=record_(email);if(!current)throw new Error('Distributor not found.');if(stateText_(current.status)==='stopped')throw new Error('Service stopped. Contact admin.');if(stateText_(current.renewalRequested)==='true')throw new Error('A renewal is already awaiting admin review.');if(Date.now()<expiry_(current))throw new Error('Renewal is available after expiry.');
  const requestId=randomToken_(),ref=storePortalImage_(data.imageData,email,'payment');
  try{claimTransaction_(txn,email,'renewal',requestId);const result=updateDistributor_(email,{status:'Pending',paymentStatus:'Pending',approvalGranted:false,approved:false,accessApproved:false,paymentPlan:selectedPlan.label,paymentAmount:selectedPlan.amount,paymentTxnId:txn,paymentScreenshot:ref,renewalRequested:true,renewalPlan:selectedPlan.label,renewalAmount:selectedPlan.amount,renewalTxnId:txn,renewalScreenshot:ref,renewalRequestedAt:Date.now(),paymentRequestId:requestId,paymentRequestedAt:Date.now(),approvalNote:'Renewal awaiting admin review'});if(!result.success)throw new Error(result.error);return result;}catch(e){releaseTransaction_(email,'renewal',requestId);discardManagedImage_(ref);throw e;}
}





function json_(data) {
  return ContentService.createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}

function renewalPlan_(value) {
  const key = String(value || '').trim().toLowerCase();
  if (key === '1 month' || key === '1month') return { label: '1 Month', amount: '₹36', days: 30 };
  if (key === '1 year' || key === '1year') return { label: '1 Year', amount: '₹319', days: 365 };
  return null;
}

function reviewPayment_(data){
  return withLock_(()=>{const email=email_(data.email),record=record_(email);if(!record)throw new Error('Distributor not found.');if(stateText_(record.paymentStatus)!=='pending')throw new Error('This request is no longer pending. Refresh the admin panel.');
    const expected=String(record.paymentRequestId||''),provided=String(data.requestId||'');if(expected&&provided!==expected)throw new Error('Request changed or already reviewed. Refresh the admin panel.');
    const renewal=stateText_(record.renewalRequested)==='true',plan=renewalPlan_(renewal?record.renewalPlan:record.paymentPlan),approved=String(data.approved)==='true';if(![true,false,'true','false'].includes(data.approved))throw new Error('Invalid decision.');if(approved&&(!plan||!(renewal?record.renewalScreenshot:record.paymentScreenshot)))throw new Error('Valid plan and payment screenshot required.');
    const now=Date.now(),changes={approved,approvalGranted:approved,accessApproved:approved,status:approved?'Active':'Rejected',paymentStatus:approved?'Approved':'Rejected',renewalRequested:false,approvalNote:approved?'Payment approved by admin':'Payment rejected by admin'};
    if(approved){changes.paymentApprovedAt=now;changes.expiryTime=now+plan.days*86400000;changes.paymentPlan=plan.label;changes.paymentAmount=plan.amount;}
    const result=updateDistributor_(email,changes);if(!result.success)throw new Error(result.error);try{scheduleImageRetention_([record.paymentScreenshot,record.renewalScreenshot],now+RETENTION_MS_);reviewTransaction_(expected,approved?'Approved':'Rejected');}catch(e){console.log('Post-review retention metadata will be repaired by cleanup.');}return result;
  });
}
/* Vendored hash.js 1.1.7 and dependencies. MIT licenses retained below.
hash.js


This software is licensed under the MIT License.

Copyright Fedor Indutny, 2014.

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the
following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
USE OR OTHER DEALINGS IN THE SOFTWARE.


inherits
The ISC License

Copyright (c) Isaac Z. Schlueter

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.



minimalistic-assert
Copyright 2015 Calvin Metcalf

Permission to use, copy, modify, and/or distribute this software for any purpose
with or without fee is hereby granted, provided that the above copyright notice
and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
*/
var PortalHash = (function(){const modules=[function(module,exports,load){
var hash = exports;

hash.utils = load(1);
hash.common = load(4);
hash.sha = load(5);
hash.ripemd = load(12);
hash.hmac = load(13);

// Proxy hash functions to the main object
hash.sha1 = hash.sha.sha1;
hash.sha256 = hash.sha.sha256;
hash.sha224 = hash.sha.sha224;
hash.sha384 = hash.sha.sha384;
hash.sha512 = hash.sha.sha512;
hash.ripemd160 = hash.ripemd.ripemd160;

},
function(module,exports,load){
'use strict';

var assert = load(2);
var inherits = load(3);

exports.inherits = inherits;

function isSurrogatePair(msg, i) {
  if ((msg.charCodeAt(i) & 0xFC00) !== 0xD800) {
    return false;
  }
  if (i < 0 || i + 1 >= msg.length) {
    return false;
  }
  return (msg.charCodeAt(i + 1) & 0xFC00) === 0xDC00;
}

function toArray(msg, enc) {
  if (Array.isArray(msg))
    return msg.slice();
  if (!msg)
    return [];
  var res = [];
  if (typeof msg === 'string') {
    if (!enc) {
      // Inspired by stringToUtf8ByteArray() in closure-library by Google
      // https://github.com/google/closure-library/blob/8598d87242af59aac233270742c8984e2b2bdbe0/closure/goog/crypt/crypt.js#L117-L143
      // Apache License 2.0
      // https://github.com/google/closure-library/blob/master/LICENSE
      var p = 0;
      for (var i = 0; i < msg.length; i++) {
        var c = msg.charCodeAt(i);
        if (c < 128) {
          res[p++] = c;
        } else if (c < 2048) {
          res[p++] = (c >> 6) | 192;
          res[p++] = (c & 63) | 128;
        } else if (isSurrogatePair(msg, i)) {
          c = 0x10000 + ((c & 0x03FF) << 10) + (msg.charCodeAt(++i) & 0x03FF);
          res[p++] = (c >> 18) | 240;
          res[p++] = ((c >> 12) & 63) | 128;
          res[p++] = ((c >> 6) & 63) | 128;
          res[p++] = (c & 63) | 128;
        } else {
          res[p++] = (c >> 12) | 224;
          res[p++] = ((c >> 6) & 63) | 128;
          res[p++] = (c & 63) | 128;
        }
      }
    } else if (enc === 'hex') {
      msg = msg.replace(/[^a-z0-9]+/ig, '');
      if (msg.length % 2 !== 0)
        msg = '0' + msg;
      for (i = 0; i < msg.length; i += 2)
        res.push(parseInt(msg[i] + msg[i + 1], 16));
    }
  } else {
    for (i = 0; i < msg.length; i++)
      res[i] = msg[i] | 0;
  }
  return res;
}
exports.toArray = toArray;

function toHex(msg) {
  var res = '';
  for (var i = 0; i < msg.length; i++)
    res += zero2(msg[i].toString(16));
  return res;
}
exports.toHex = toHex;

function htonl(w) {
  var res = (w >>> 24) |
            ((w >>> 8) & 0xff00) |
            ((w << 8) & 0xff0000) |
            ((w & 0xff) << 24);
  return res >>> 0;
}
exports.htonl = htonl;

function toHex32(msg, endian) {
  var res = '';
  for (var i = 0; i < msg.length; i++) {
    var w = msg[i];
    if (endian === 'little')
      w = htonl(w);
    res += zero8(w.toString(16));
  }
  return res;
}
exports.toHex32 = toHex32;

function zero2(word) {
  if (word.length === 1)
    return '0' + word;
  else
    return word;
}
exports.zero2 = zero2;

function zero8(word) {
  if (word.length === 7)
    return '0' + word;
  else if (word.length === 6)
    return '00' + word;
  else if (word.length === 5)
    return '000' + word;
  else if (word.length === 4)
    return '0000' + word;
  else if (word.length === 3)
    return '00000' + word;
  else if (word.length === 2)
    return '000000' + word;
  else if (word.length === 1)
    return '0000000' + word;
  else
    return word;
}
exports.zero8 = zero8;

function join32(msg, start, end, endian) {
  var len = end - start;
  assert(len % 4 === 0);
  var res = new Array(len / 4);
  for (var i = 0, k = start; i < res.length; i++, k += 4) {
    var w;
    if (endian === 'big')
      w = (msg[k] << 24) | (msg[k + 1] << 16) | (msg[k + 2] << 8) | msg[k + 3];
    else
      w = (msg[k + 3] << 24) | (msg[k + 2] << 16) | (msg[k + 1] << 8) | msg[k];
    res[i] = w >>> 0;
  }
  return res;
}
exports.join32 = join32;

function split32(msg, endian) {
  var res = new Array(msg.length * 4);
  for (var i = 0, k = 0; i < msg.length; i++, k += 4) {
    var m = msg[i];
    if (endian === 'big') {
      res[k] = m >>> 24;
      res[k + 1] = (m >>> 16) & 0xff;
      res[k + 2] = (m >>> 8) & 0xff;
      res[k + 3] = m & 0xff;
    } else {
      res[k + 3] = m >>> 24;
      res[k + 2] = (m >>> 16) & 0xff;
      res[k + 1] = (m >>> 8) & 0xff;
      res[k] = m & 0xff;
    }
  }
  return res;
}
exports.split32 = split32;

function rotr32(w, b) {
  return (w >>> b) | (w << (32 - b));
}
exports.rotr32 = rotr32;

function rotl32(w, b) {
  return (w << b) | (w >>> (32 - b));
}
exports.rotl32 = rotl32;

function sum32(a, b) {
  return (a + b) >>> 0;
}
exports.sum32 = sum32;

function sum32_3(a, b, c) {
  return (a + b + c) >>> 0;
}
exports.sum32_3 = sum32_3;

function sum32_4(a, b, c, d) {
  return (a + b + c + d) >>> 0;
}
exports.sum32_4 = sum32_4;

function sum32_5(a, b, c, d, e) {
  return (a + b + c + d + e) >>> 0;
}
exports.sum32_5 = sum32_5;

function sum64(buf, pos, ah, al) {
  var bh = buf[pos];
  var bl = buf[pos + 1];

  var lo = (al + bl) >>> 0;
  var hi = (lo < al ? 1 : 0) + ah + bh;
  buf[pos] = hi >>> 0;
  buf[pos + 1] = lo;
}
exports.sum64 = sum64;

function sum64_hi(ah, al, bh, bl) {
  var lo = (al + bl) >>> 0;
  var hi = (lo < al ? 1 : 0) + ah + bh;
  return hi >>> 0;
}
exports.sum64_hi = sum64_hi;

function sum64_lo(ah, al, bh, bl) {
  var lo = al + bl;
  return lo >>> 0;
}
exports.sum64_lo = sum64_lo;

function sum64_4_hi(ah, al, bh, bl, ch, cl, dh, dl) {
  var carry = 0;
  var lo = al;
  lo = (lo + bl) >>> 0;
  carry += lo < al ? 1 : 0;
  lo = (lo + cl) >>> 0;
  carry += lo < cl ? 1 : 0;
  lo = (lo + dl) >>> 0;
  carry += lo < dl ? 1 : 0;

  var hi = ah + bh + ch + dh + carry;
  return hi >>> 0;
}
exports.sum64_4_hi = sum64_4_hi;

function sum64_4_lo(ah, al, bh, bl, ch, cl, dh, dl) {
  var lo = al + bl + cl + dl;
  return lo >>> 0;
}
exports.sum64_4_lo = sum64_4_lo;

function sum64_5_hi(ah, al, bh, bl, ch, cl, dh, dl, eh, el) {
  var carry = 0;
  var lo = al;
  lo = (lo + bl) >>> 0;
  carry += lo < al ? 1 : 0;
  lo = (lo + cl) >>> 0;
  carry += lo < cl ? 1 : 0;
  lo = (lo + dl) >>> 0;
  carry += lo < dl ? 1 : 0;
  lo = (lo + el) >>> 0;
  carry += lo < el ? 1 : 0;

  var hi = ah + bh + ch + dh + eh + carry;
  return hi >>> 0;
}
exports.sum64_5_hi = sum64_5_hi;

function sum64_5_lo(ah, al, bh, bl, ch, cl, dh, dl, eh, el) {
  var lo = al + bl + cl + dl + el;

  return lo >>> 0;
}
exports.sum64_5_lo = sum64_5_lo;

function rotr64_hi(ah, al, num) {
  var r = (al << (32 - num)) | (ah >>> num);
  return r >>> 0;
}
exports.rotr64_hi = rotr64_hi;

function rotr64_lo(ah, al, num) {
  var r = (ah << (32 - num)) | (al >>> num);
  return r >>> 0;
}
exports.rotr64_lo = rotr64_lo;

function shr64_hi(ah, al, num) {
  return ah >>> num;
}
exports.shr64_hi = shr64_hi;

function shr64_lo(ah, al, num) {
  var r = (ah << (32 - num)) | (al >>> num);
  return r >>> 0;
}
exports.shr64_lo = shr64_lo;

},
function(module,exports,load){
module.exports = assert;

function assert(val, msg) {
  if (!val)
    throw new Error(msg || 'Assertion failed');
}

assert.equal = function assertEqual(l, r, msg) {
  if (l != r)
    throw new Error(msg || ('Assertion failed: ' + l + ' != ' + r));
};

},
function(module,exports,load){
if (typeof Object.create === 'function') {
  // implementation from standard node.js 'util' module
  module.exports = function inherits(ctor, superCtor) {
    if (superCtor) {
      ctor.super_ = superCtor
      ctor.prototype = Object.create(superCtor.prototype, {
        constructor: {
          value: ctor,
          enumerable: false,
          writable: true,
          configurable: true
        }
      })
    }
  };
} else {
  // old school shim for old browsers
  module.exports = function inherits(ctor, superCtor) {
    if (superCtor) {
      ctor.super_ = superCtor
      var TempCtor = function () {}
      TempCtor.prototype = superCtor.prototype
      ctor.prototype = new TempCtor()
      ctor.prototype.constructor = ctor
    }
  }
}

},
function(module,exports,load){
'use strict';

var utils = load(1);
var assert = load(2);

function BlockHash() {
  this.pending = null;
  this.pendingTotal = 0;
  this.blockSize = this.constructor.blockSize;
  this.outSize = this.constructor.outSize;
  this.hmacStrength = this.constructor.hmacStrength;
  this.padLength = this.constructor.padLength / 8;
  this.endian = 'big';

  this._delta8 = this.blockSize / 8;
  this._delta32 = this.blockSize / 32;
}
exports.BlockHash = BlockHash;

BlockHash.prototype.update = function update(msg, enc) {
  // Convert message to array, pad it, and join into 32bit blocks
  msg = utils.toArray(msg, enc);
  if (!this.pending)
    this.pending = msg;
  else
    this.pending = this.pending.concat(msg);
  this.pendingTotal += msg.length;

  // Enough data, try updating
  if (this.pending.length >= this._delta8) {
    msg = this.pending;

    // Process pending data in blocks
    var r = msg.length % this._delta8;
    this.pending = msg.slice(msg.length - r, msg.length);
    if (this.pending.length === 0)
      this.pending = null;

    msg = utils.join32(msg, 0, msg.length - r, this.endian);
    for (var i = 0; i < msg.length; i += this._delta32)
      this._update(msg, i, i + this._delta32);
  }

  return this;
};

BlockHash.prototype.digest = function digest(enc) {
  this.update(this._pad());
  assert(this.pending === null);

  return this._digest(enc);
};

BlockHash.prototype._pad = function pad() {
  var len = this.pendingTotal;
  var bytes = this._delta8;
  var k = bytes - ((len + this.padLength) % bytes);
  var res = new Array(k + this.padLength);
  res[0] = 0x80;
  for (var i = 1; i < k; i++)
    res[i] = 0;

  // Append length
  len <<= 3;
  if (this.endian === 'big') {
    for (var t = 8; t < this.padLength; t++)
      res[i++] = 0;

    res[i++] = 0;
    res[i++] = 0;
    res[i++] = 0;
    res[i++] = 0;
    res[i++] = (len >>> 24) & 0xff;
    res[i++] = (len >>> 16) & 0xff;
    res[i++] = (len >>> 8) & 0xff;
    res[i++] = len & 0xff;
  } else {
    res[i++] = len & 0xff;
    res[i++] = (len >>> 8) & 0xff;
    res[i++] = (len >>> 16) & 0xff;
    res[i++] = (len >>> 24) & 0xff;
    res[i++] = 0;
    res[i++] = 0;
    res[i++] = 0;
    res[i++] = 0;

    for (t = 8; t < this.padLength; t++)
      res[i++] = 0;
  }

  return res;
};

},
function(module,exports,load){
'use strict';

exports.sha1 = load(6);
exports.sha224 = load(8);
exports.sha256 = load(9);
exports.sha384 = load(10);
exports.sha512 = load(11);

},
function(module,exports,load){
'use strict';

var utils = load(1);
var common = load(4);
var shaCommon = load(7);

var rotl32 = utils.rotl32;
var sum32 = utils.sum32;
var sum32_5 = utils.sum32_5;
var ft_1 = shaCommon.ft_1;
var BlockHash = common.BlockHash;

var sha1_K = [
  0x5A827999, 0x6ED9EBA1,
  0x8F1BBCDC, 0xCA62C1D6
];

function SHA1() {
  if (!(this instanceof SHA1))
    return new SHA1();

  BlockHash.call(this);
  this.h = [
    0x67452301, 0xefcdab89, 0x98badcfe,
    0x10325476, 0xc3d2e1f0 ];
  this.W = new Array(80);
}

utils.inherits(SHA1, BlockHash);
module.exports = SHA1;

SHA1.blockSize = 512;
SHA1.outSize = 160;
SHA1.hmacStrength = 80;
SHA1.padLength = 64;

SHA1.prototype._update = function _update(msg, start) {
  var W = this.W;

  for (var i = 0; i < 16; i++)
    W[i] = msg[start + i];

  for(; i < W.length; i++)
    W[i] = rotl32(W[i - 3] ^ W[i - 8] ^ W[i - 14] ^ W[i - 16], 1);

  var a = this.h[0];
  var b = this.h[1];
  var c = this.h[2];
  var d = this.h[3];
  var e = this.h[4];

  for (i = 0; i < W.length; i++) {
    var s = ~~(i / 20);
    var t = sum32_5(rotl32(a, 5), ft_1(s, b, c, d), e, W[i], sha1_K[s]);
    e = d;
    d = c;
    c = rotl32(b, 30);
    b = a;
    a = t;
  }

  this.h[0] = sum32(this.h[0], a);
  this.h[1] = sum32(this.h[1], b);
  this.h[2] = sum32(this.h[2], c);
  this.h[3] = sum32(this.h[3], d);
  this.h[4] = sum32(this.h[4], e);
};

SHA1.prototype._digest = function digest(enc) {
  if (enc === 'hex')
    return utils.toHex32(this.h, 'big');
  else
    return utils.split32(this.h, 'big');
};

},
function(module,exports,load){
'use strict';

var utils = load(1);
var rotr32 = utils.rotr32;

function ft_1(s, x, y, z) {
  if (s === 0)
    return ch32(x, y, z);
  if (s === 1 || s === 3)
    return p32(x, y, z);
  if (s === 2)
    return maj32(x, y, z);
}
exports.ft_1 = ft_1;

function ch32(x, y, z) {
  return (x & y) ^ ((~x) & z);
}
exports.ch32 = ch32;

function maj32(x, y, z) {
  return (x & y) ^ (x & z) ^ (y & z);
}
exports.maj32 = maj32;

function p32(x, y, z) {
  return x ^ y ^ z;
}
exports.p32 = p32;

function s0_256(x) {
  return rotr32(x, 2) ^ rotr32(x, 13) ^ rotr32(x, 22);
}
exports.s0_256 = s0_256;

function s1_256(x) {
  return rotr32(x, 6) ^ rotr32(x, 11) ^ rotr32(x, 25);
}
exports.s1_256 = s1_256;

function g0_256(x) {
  return rotr32(x, 7) ^ rotr32(x, 18) ^ (x >>> 3);
}
exports.g0_256 = g0_256;

function g1_256(x) {
  return rotr32(x, 17) ^ rotr32(x, 19) ^ (x >>> 10);
}
exports.g1_256 = g1_256;

},
function(module,exports,load){
'use strict';

var utils = load(1);
var SHA256 = load(9);

function SHA224() {
  if (!(this instanceof SHA224))
    return new SHA224();

  SHA256.call(this);
  this.h = [
    0xc1059ed8, 0x367cd507, 0x3070dd17, 0xf70e5939,
    0xffc00b31, 0x68581511, 0x64f98fa7, 0xbefa4fa4 ];
}
utils.inherits(SHA224, SHA256);
module.exports = SHA224;

SHA224.blockSize = 512;
SHA224.outSize = 224;
SHA224.hmacStrength = 192;
SHA224.padLength = 64;

SHA224.prototype._digest = function digest(enc) {
  // Just truncate output
  if (enc === 'hex')
    return utils.toHex32(this.h.slice(0, 7), 'big');
  else
    return utils.split32(this.h.slice(0, 7), 'big');
};


},
function(module,exports,load){
'use strict';

var utils = load(1);
var common = load(4);
var shaCommon = load(7);
var assert = load(2);

var sum32 = utils.sum32;
var sum32_4 = utils.sum32_4;
var sum32_5 = utils.sum32_5;
var ch32 = shaCommon.ch32;
var maj32 = shaCommon.maj32;
var s0_256 = shaCommon.s0_256;
var s1_256 = shaCommon.s1_256;
var g0_256 = shaCommon.g0_256;
var g1_256 = shaCommon.g1_256;

var BlockHash = common.BlockHash;

var sha256_K = [
  0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
  0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
  0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
  0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
  0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
  0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
  0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
  0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
  0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
  0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
  0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
  0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
  0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
  0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
  0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
  0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
];

function SHA256() {
  if (!(this instanceof SHA256))
    return new SHA256();

  BlockHash.call(this);
  this.h = [
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
  ];
  this.k = sha256_K;
  this.W = new Array(64);
}
utils.inherits(SHA256, BlockHash);
module.exports = SHA256;

SHA256.blockSize = 512;
SHA256.outSize = 256;
SHA256.hmacStrength = 192;
SHA256.padLength = 64;

SHA256.prototype._update = function _update(msg, start) {
  var W = this.W;

  for (var i = 0; i < 16; i++)
    W[i] = msg[start + i];
  for (; i < W.length; i++)
    W[i] = sum32_4(g1_256(W[i - 2]), W[i - 7], g0_256(W[i - 15]), W[i - 16]);

  var a = this.h[0];
  var b = this.h[1];
  var c = this.h[2];
  var d = this.h[3];
  var e = this.h[4];
  var f = this.h[5];
  var g = this.h[6];
  var h = this.h[7];

  assert(this.k.length === W.length);
  for (i = 0; i < W.length; i++) {
    var T1 = sum32_5(h, s1_256(e), ch32(e, f, g), this.k[i], W[i]);
    var T2 = sum32(s0_256(a), maj32(a, b, c));
    h = g;
    g = f;
    f = e;
    e = sum32(d, T1);
    d = c;
    c = b;
    b = a;
    a = sum32(T1, T2);
  }

  this.h[0] = sum32(this.h[0], a);
  this.h[1] = sum32(this.h[1], b);
  this.h[2] = sum32(this.h[2], c);
  this.h[3] = sum32(this.h[3], d);
  this.h[4] = sum32(this.h[4], e);
  this.h[5] = sum32(this.h[5], f);
  this.h[6] = sum32(this.h[6], g);
  this.h[7] = sum32(this.h[7], h);
};

SHA256.prototype._digest = function digest(enc) {
  if (enc === 'hex')
    return utils.toHex32(this.h, 'big');
  else
    return utils.split32(this.h, 'big');
};

},
function(module,exports,load){
'use strict';

var utils = load(1);

var SHA512 = load(11);

function SHA384() {
  if (!(this instanceof SHA384))
    return new SHA384();

  SHA512.call(this);
  this.h = [
    0xcbbb9d5d, 0xc1059ed8,
    0x629a292a, 0x367cd507,
    0x9159015a, 0x3070dd17,
    0x152fecd8, 0xf70e5939,
    0x67332667, 0xffc00b31,
    0x8eb44a87, 0x68581511,
    0xdb0c2e0d, 0x64f98fa7,
    0x47b5481d, 0xbefa4fa4 ];
}
utils.inherits(SHA384, SHA512);
module.exports = SHA384;

SHA384.blockSize = 1024;
SHA384.outSize = 384;
SHA384.hmacStrength = 192;
SHA384.padLength = 128;

SHA384.prototype._digest = function digest(enc) {
  if (enc === 'hex')
    return utils.toHex32(this.h.slice(0, 12), 'big');
  else
    return utils.split32(this.h.slice(0, 12), 'big');
};

},
function(module,exports,load){
'use strict';

var utils = load(1);
var common = load(4);
var assert = load(2);

var rotr64_hi = utils.rotr64_hi;
var rotr64_lo = utils.rotr64_lo;
var shr64_hi = utils.shr64_hi;
var shr64_lo = utils.shr64_lo;
var sum64 = utils.sum64;
var sum64_hi = utils.sum64_hi;
var sum64_lo = utils.sum64_lo;
var sum64_4_hi = utils.sum64_4_hi;
var sum64_4_lo = utils.sum64_4_lo;
var sum64_5_hi = utils.sum64_5_hi;
var sum64_5_lo = utils.sum64_5_lo;

var BlockHash = common.BlockHash;

var sha512_K = [
  0x428a2f98, 0xd728ae22, 0x71374491, 0x23ef65cd,
  0xb5c0fbcf, 0xec4d3b2f, 0xe9b5dba5, 0x8189dbbc,
  0x3956c25b, 0xf348b538, 0x59f111f1, 0xb605d019,
  0x923f82a4, 0xaf194f9b, 0xab1c5ed5, 0xda6d8118,
  0xd807aa98, 0xa3030242, 0x12835b01, 0x45706fbe,
  0x243185be, 0x4ee4b28c, 0x550c7dc3, 0xd5ffb4e2,
  0x72be5d74, 0xf27b896f, 0x80deb1fe, 0x3b1696b1,
  0x9bdc06a7, 0x25c71235, 0xc19bf174, 0xcf692694,
  0xe49b69c1, 0x9ef14ad2, 0xefbe4786, 0x384f25e3,
  0x0fc19dc6, 0x8b8cd5b5, 0x240ca1cc, 0x77ac9c65,
  0x2de92c6f, 0x592b0275, 0x4a7484aa, 0x6ea6e483,
  0x5cb0a9dc, 0xbd41fbd4, 0x76f988da, 0x831153b5,
  0x983e5152, 0xee66dfab, 0xa831c66d, 0x2db43210,
  0xb00327c8, 0x98fb213f, 0xbf597fc7, 0xbeef0ee4,
  0xc6e00bf3, 0x3da88fc2, 0xd5a79147, 0x930aa725,
  0x06ca6351, 0xe003826f, 0x14292967, 0x0a0e6e70,
  0x27b70a85, 0x46d22ffc, 0x2e1b2138, 0x5c26c926,
  0x4d2c6dfc, 0x5ac42aed, 0x53380d13, 0x9d95b3df,
  0x650a7354, 0x8baf63de, 0x766a0abb, 0x3c77b2a8,
  0x81c2c92e, 0x47edaee6, 0x92722c85, 0x1482353b,
  0xa2bfe8a1, 0x4cf10364, 0xa81a664b, 0xbc423001,
  0xc24b8b70, 0xd0f89791, 0xc76c51a3, 0x0654be30,
  0xd192e819, 0xd6ef5218, 0xd6990624, 0x5565a910,
  0xf40e3585, 0x5771202a, 0x106aa070, 0x32bbd1b8,
  0x19a4c116, 0xb8d2d0c8, 0x1e376c08, 0x5141ab53,
  0x2748774c, 0xdf8eeb99, 0x34b0bcb5, 0xe19b48a8,
  0x391c0cb3, 0xc5c95a63, 0x4ed8aa4a, 0xe3418acb,
  0x5b9cca4f, 0x7763e373, 0x682e6ff3, 0xd6b2b8a3,
  0x748f82ee, 0x5defb2fc, 0x78a5636f, 0x43172f60,
  0x84c87814, 0xa1f0ab72, 0x8cc70208, 0x1a6439ec,
  0x90befffa, 0x23631e28, 0xa4506ceb, 0xde82bde9,
  0xbef9a3f7, 0xb2c67915, 0xc67178f2, 0xe372532b,
  0xca273ece, 0xea26619c, 0xd186b8c7, 0x21c0c207,
  0xeada7dd6, 0xcde0eb1e, 0xf57d4f7f, 0xee6ed178,
  0x06f067aa, 0x72176fba, 0x0a637dc5, 0xa2c898a6,
  0x113f9804, 0xbef90dae, 0x1b710b35, 0x131c471b,
  0x28db77f5, 0x23047d84, 0x32caab7b, 0x40c72493,
  0x3c9ebe0a, 0x15c9bebc, 0x431d67c4, 0x9c100d4c,
  0x4cc5d4be, 0xcb3e42b6, 0x597f299c, 0xfc657e2a,
  0x5fcb6fab, 0x3ad6faec, 0x6c44198c, 0x4a475817
];

function SHA512() {
  if (!(this instanceof SHA512))
    return new SHA512();

  BlockHash.call(this);
  this.h = [
    0x6a09e667, 0xf3bcc908,
    0xbb67ae85, 0x84caa73b,
    0x3c6ef372, 0xfe94f82b,
    0xa54ff53a, 0x5f1d36f1,
    0x510e527f, 0xade682d1,
    0x9b05688c, 0x2b3e6c1f,
    0x1f83d9ab, 0xfb41bd6b,
    0x5be0cd19, 0x137e2179 ];
  this.k = sha512_K;
  this.W = new Array(160);
}
utils.inherits(SHA512, BlockHash);
module.exports = SHA512;

SHA512.blockSize = 1024;
SHA512.outSize = 512;
SHA512.hmacStrength = 192;
SHA512.padLength = 128;

SHA512.prototype._prepareBlock = function _prepareBlock(msg, start) {
  var W = this.W;

  // 32 x 32bit words
  for (var i = 0; i < 32; i++)
    W[i] = msg[start + i];
  for (; i < W.length; i += 2) {
    var c0_hi = g1_512_hi(W[i - 4], W[i - 3]);  // i - 2
    var c0_lo = g1_512_lo(W[i - 4], W[i - 3]);
    var c1_hi = W[i - 14];  // i - 7
    var c1_lo = W[i - 13];
    var c2_hi = g0_512_hi(W[i - 30], W[i - 29]);  // i - 15
    var c2_lo = g0_512_lo(W[i - 30], W[i - 29]);
    var c3_hi = W[i - 32];  // i - 16
    var c3_lo = W[i - 31];

    W[i] = sum64_4_hi(
      c0_hi, c0_lo,
      c1_hi, c1_lo,
      c2_hi, c2_lo,
      c3_hi, c3_lo);
    W[i + 1] = sum64_4_lo(
      c0_hi, c0_lo,
      c1_hi, c1_lo,
      c2_hi, c2_lo,
      c3_hi, c3_lo);
  }
};

SHA512.prototype._update = function _update(msg, start) {
  this._prepareBlock(msg, start);

  var W = this.W;

  var ah = this.h[0];
  var al = this.h[1];
  var bh = this.h[2];
  var bl = this.h[3];
  var ch = this.h[4];
  var cl = this.h[5];
  var dh = this.h[6];
  var dl = this.h[7];
  var eh = this.h[8];
  var el = this.h[9];
  var fh = this.h[10];
  var fl = this.h[11];
  var gh = this.h[12];
  var gl = this.h[13];
  var hh = this.h[14];
  var hl = this.h[15];

  assert(this.k.length === W.length);
  for (var i = 0; i < W.length; i += 2) {
    var c0_hi = hh;
    var c0_lo = hl;
    var c1_hi = s1_512_hi(eh, el);
    var c1_lo = s1_512_lo(eh, el);
    var c2_hi = ch64_hi(eh, el, fh, fl, gh, gl);
    var c2_lo = ch64_lo(eh, el, fh, fl, gh, gl);
    var c3_hi = this.k[i];
    var c3_lo = this.k[i + 1];
    var c4_hi = W[i];
    var c4_lo = W[i + 1];

    var T1_hi = sum64_5_hi(
      c0_hi, c0_lo,
      c1_hi, c1_lo,
      c2_hi, c2_lo,
      c3_hi, c3_lo,
      c4_hi, c4_lo);
    var T1_lo = sum64_5_lo(
      c0_hi, c0_lo,
      c1_hi, c1_lo,
      c2_hi, c2_lo,
      c3_hi, c3_lo,
      c4_hi, c4_lo);

    c0_hi = s0_512_hi(ah, al);
    c0_lo = s0_512_lo(ah, al);
    c1_hi = maj64_hi(ah, al, bh, bl, ch, cl);
    c1_lo = maj64_lo(ah, al, bh, bl, ch, cl);

    var T2_hi = sum64_hi(c0_hi, c0_lo, c1_hi, c1_lo);
    var T2_lo = sum64_lo(c0_hi, c0_lo, c1_hi, c1_lo);

    hh = gh;
    hl = gl;

    gh = fh;
    gl = fl;

    fh = eh;
    fl = el;

    eh = sum64_hi(dh, dl, T1_hi, T1_lo);
    el = sum64_lo(dl, dl, T1_hi, T1_lo);

    dh = ch;
    dl = cl;

    ch = bh;
    cl = bl;

    bh = ah;
    bl = al;

    ah = sum64_hi(T1_hi, T1_lo, T2_hi, T2_lo);
    al = sum64_lo(T1_hi, T1_lo, T2_hi, T2_lo);
  }

  sum64(this.h, 0, ah, al);
  sum64(this.h, 2, bh, bl);
  sum64(this.h, 4, ch, cl);
  sum64(this.h, 6, dh, dl);
  sum64(this.h, 8, eh, el);
  sum64(this.h, 10, fh, fl);
  sum64(this.h, 12, gh, gl);
  sum64(this.h, 14, hh, hl);
};

SHA512.prototype._digest = function digest(enc) {
  if (enc === 'hex')
    return utils.toHex32(this.h, 'big');
  else
    return utils.split32(this.h, 'big');
};

function ch64_hi(xh, xl, yh, yl, zh) {
  var r = (xh & yh) ^ ((~xh) & zh);
  if (r < 0)
    r += 0x100000000;
  return r;
}

function ch64_lo(xh, xl, yh, yl, zh, zl) {
  var r = (xl & yl) ^ ((~xl) & zl);
  if (r < 0)
    r += 0x100000000;
  return r;
}

function maj64_hi(xh, xl, yh, yl, zh) {
  var r = (xh & yh) ^ (xh & zh) ^ (yh & zh);
  if (r < 0)
    r += 0x100000000;
  return r;
}

function maj64_lo(xh, xl, yh, yl, zh, zl) {
  var r = (xl & yl) ^ (xl & zl) ^ (yl & zl);
  if (r < 0)
    r += 0x100000000;
  return r;
}

function s0_512_hi(xh, xl) {
  var c0_hi = rotr64_hi(xh, xl, 28);
  var c1_hi = rotr64_hi(xl, xh, 2);  // 34
  var c2_hi = rotr64_hi(xl, xh, 7);  // 39

  var r = c0_hi ^ c1_hi ^ c2_hi;
  if (r < 0)
    r += 0x100000000;
  return r;
}

function s0_512_lo(xh, xl) {
  var c0_lo = rotr64_lo(xh, xl, 28);
  var c1_lo = rotr64_lo(xl, xh, 2);  // 34
  var c2_lo = rotr64_lo(xl, xh, 7);  // 39

  var r = c0_lo ^ c1_lo ^ c2_lo;
  if (r < 0)
    r += 0x100000000;
  return r;
}

function s1_512_hi(xh, xl) {
  var c0_hi = rotr64_hi(xh, xl, 14);
  var c1_hi = rotr64_hi(xh, xl, 18);
  var c2_hi = rotr64_hi(xl, xh, 9);  // 41

  var r = c0_hi ^ c1_hi ^ c2_hi;
  if (r < 0)
    r += 0x100000000;
  return r;
}

function s1_512_lo(xh, xl) {
  var c0_lo = rotr64_lo(xh, xl, 14);
  var c1_lo = rotr64_lo(xh, xl, 18);
  var c2_lo = rotr64_lo(xl, xh, 9);  // 41

  var r = c0_lo ^ c1_lo ^ c2_lo;
  if (r < 0)
    r += 0x100000000;
  return r;
}

function g0_512_hi(xh, xl) {
  var c0_hi = rotr64_hi(xh, xl, 1);
  var c1_hi = rotr64_hi(xh, xl, 8);
  var c2_hi = shr64_hi(xh, xl, 7);

  var r = c0_hi ^ c1_hi ^ c2_hi;
  if (r < 0)
    r += 0x100000000;
  return r;
}

function g0_512_lo(xh, xl) {
  var c0_lo = rotr64_lo(xh, xl, 1);
  var c1_lo = rotr64_lo(xh, xl, 8);
  var c2_lo = shr64_lo(xh, xl, 7);

  var r = c0_lo ^ c1_lo ^ c2_lo;
  if (r < 0)
    r += 0x100000000;
  return r;
}

function g1_512_hi(xh, xl) {
  var c0_hi = rotr64_hi(xh, xl, 19);
  var c1_hi = rotr64_hi(xl, xh, 29);  // 61
  var c2_hi = shr64_hi(xh, xl, 6);

  var r = c0_hi ^ c1_hi ^ c2_hi;
  if (r < 0)
    r += 0x100000000;
  return r;
}

function g1_512_lo(xh, xl) {
  var c0_lo = rotr64_lo(xh, xl, 19);
  var c1_lo = rotr64_lo(xl, xh, 29);  // 61
  var c2_lo = shr64_lo(xh, xl, 6);

  var r = c0_lo ^ c1_lo ^ c2_lo;
  if (r < 0)
    r += 0x100000000;
  return r;
}

},
function(module,exports,load){
'use strict';

var utils = load(1);
var common = load(4);

var rotl32 = utils.rotl32;
var sum32 = utils.sum32;
var sum32_3 = utils.sum32_3;
var sum32_4 = utils.sum32_4;
var BlockHash = common.BlockHash;

function RIPEMD160() {
  if (!(this instanceof RIPEMD160))
    return new RIPEMD160();

  BlockHash.call(this);

  this.h = [ 0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476, 0xc3d2e1f0 ];
  this.endian = 'little';
}
utils.inherits(RIPEMD160, BlockHash);
exports.ripemd160 = RIPEMD160;

RIPEMD160.blockSize = 512;
RIPEMD160.outSize = 160;
RIPEMD160.hmacStrength = 192;
RIPEMD160.padLength = 64;

RIPEMD160.prototype._update = function update(msg, start) {
  var A = this.h[0];
  var B = this.h[1];
  var C = this.h[2];
  var D = this.h[3];
  var E = this.h[4];
  var Ah = A;
  var Bh = B;
  var Ch = C;
  var Dh = D;
  var Eh = E;
  for (var j = 0; j < 80; j++) {
    var T = sum32(
      rotl32(
        sum32_4(A, f(j, B, C, D), msg[r[j] + start], K(j)),
        s[j]),
      E);
    A = E;
    E = D;
    D = rotl32(C, 10);
    C = B;
    B = T;
    T = sum32(
      rotl32(
        sum32_4(Ah, f(79 - j, Bh, Ch, Dh), msg[rh[j] + start], Kh(j)),
        sh[j]),
      Eh);
    Ah = Eh;
    Eh = Dh;
    Dh = rotl32(Ch, 10);
    Ch = Bh;
    Bh = T;
  }
  T = sum32_3(this.h[1], C, Dh);
  this.h[1] = sum32_3(this.h[2], D, Eh);
  this.h[2] = sum32_3(this.h[3], E, Ah);
  this.h[3] = sum32_3(this.h[4], A, Bh);
  this.h[4] = sum32_3(this.h[0], B, Ch);
  this.h[0] = T;
};

RIPEMD160.prototype._digest = function digest(enc) {
  if (enc === 'hex')
    return utils.toHex32(this.h, 'little');
  else
    return utils.split32(this.h, 'little');
};

function f(j, x, y, z) {
  if (j <= 15)
    return x ^ y ^ z;
  else if (j <= 31)
    return (x & y) | ((~x) & z);
  else if (j <= 47)
    return (x | (~y)) ^ z;
  else if (j <= 63)
    return (x & z) | (y & (~z));
  else
    return x ^ (y | (~z));
}

function K(j) {
  if (j <= 15)
    return 0x00000000;
  else if (j <= 31)
    return 0x5a827999;
  else if (j <= 47)
    return 0x6ed9eba1;
  else if (j <= 63)
    return 0x8f1bbcdc;
  else
    return 0xa953fd4e;
}

function Kh(j) {
  if (j <= 15)
    return 0x50a28be6;
  else if (j <= 31)
    return 0x5c4dd124;
  else if (j <= 47)
    return 0x6d703ef3;
  else if (j <= 63)
    return 0x7a6d76e9;
  else
    return 0x00000000;
}

var r = [
  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
  7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8,
  3, 10, 14, 4, 9, 15, 8, 1, 2, 7, 0, 6, 13, 11, 5, 12,
  1, 9, 11, 10, 0, 8, 12, 4, 13, 3, 7, 15, 14, 5, 6, 2,
  4, 0, 5, 9, 7, 12, 2, 10, 14, 1, 3, 8, 11, 6, 15, 13
];

var rh = [
  5, 14, 7, 0, 9, 2, 11, 4, 13, 6, 15, 8, 1, 10, 3, 12,
  6, 11, 3, 7, 0, 13, 5, 10, 14, 15, 8, 12, 4, 9, 1, 2,
  15, 5, 1, 3, 7, 14, 6, 9, 11, 8, 12, 2, 10, 0, 4, 13,
  8, 6, 4, 1, 3, 11, 15, 0, 5, 12, 2, 13, 9, 7, 10, 14,
  12, 15, 10, 4, 1, 5, 8, 7, 6, 2, 13, 14, 0, 3, 9, 11
];

var s = [
  11, 14, 15, 12, 5, 8, 7, 9, 11, 13, 14, 15, 6, 7, 9, 8,
  7, 6, 8, 13, 11, 9, 7, 15, 7, 12, 15, 9, 11, 7, 13, 12,
  11, 13, 6, 7, 14, 9, 13, 15, 14, 8, 13, 6, 5, 12, 7, 5,
  11, 12, 14, 15, 14, 15, 9, 8, 9, 14, 5, 6, 8, 6, 5, 12,
  9, 15, 5, 11, 6, 8, 13, 12, 5, 12, 13, 14, 11, 8, 5, 6
];

var sh = [
  8, 9, 9, 11, 13, 15, 15, 5, 7, 7, 8, 11, 14, 14, 12, 6,
  9, 13, 15, 7, 12, 8, 9, 11, 7, 7, 12, 7, 6, 15, 13, 11,
  9, 7, 15, 11, 8, 6, 6, 14, 12, 13, 5, 14, 13, 13, 7, 5,
  15, 5, 8, 11, 14, 14, 6, 14, 6, 9, 12, 9, 12, 5, 15, 8,
  8, 5, 12, 9, 12, 5, 14, 6, 8, 13, 6, 5, 15, 13, 11, 11
];

},
function(module,exports,load){
'use strict';

var utils = load(1);
var assert = load(2);

function Hmac(hash, key, enc) {
  if (!(this instanceof Hmac))
    return new Hmac(hash, key, enc);
  this.Hash = hash;
  this.blockSize = hash.blockSize / 8;
  this.outSize = hash.outSize / 8;
  this.inner = null;
  this.outer = null;

  this._init(utils.toArray(key, enc));
}
module.exports = Hmac;

Hmac.prototype._init = function init(key) {
  // Shorten key, if needed
  if (key.length > this.blockSize)
    key = new this.Hash().update(key).digest();
  assert(key.length <= this.blockSize);

  // Add padding to key
  for (var i = key.length; i < this.blockSize; i++)
    key.push(0);

  for (i = 0; i < key.length; i++)
    key[i] ^= 0x36;
  this.inner = new this.Hash().update(key);

  // 0x36 ^ 0x5c = 0x6a
  for (i = 0; i < key.length; i++)
    key[i] ^= 0x6a;
  this.outer = new this.Hash().update(key);
};

Hmac.prototype.update = function update(msg, enc) {
  this.inner.update(msg, enc);
  return this;
};

Hmac.prototype.digest = function digest(enc) {
  this.outer.update(this.inner.digest());
  return this.outer.digest(enc);
};

}], cache={}; function load(id){if(cache[id])return cache[id].exports;const module=cache[id]={exports:{}};modules[id](module,module.exports,load);return module.exports;}return load(0);})();
function restorePreviouslyApprovedDistributor() {
  return withLock_(() => {
    const record = accessCheckRecord_();
    const payment = stateText_(record.paymentStatus);

    if (
      stateText_(record.status) !== 'active' ||
      !['', 'approved'].includes(payment) ||
      !['', 'false'].includes(stateText_(record.renewalRequested)) ||
      record.renewalRequestedAt ||
      !Number.isFinite(expiry_(record)) ||
      expiry_(record) <= Date.now()
    ) {
      throw new Error('Account needs separate review. No changes made.');
    }

    if (payment === 'approved' && hasApproval_(record)) {
      return diagnoseDistributorAccess();
    }

    const result = updateDistributor_(record.email, {
      paymentStatus: 'Approved',
      approved: true,
      approvalGranted: true,
      accessApproved: true,
      approvalNote: String(record.approvalNote || '') +
        '\nOwner confirmed prior payment verification and approval; restored at ' +
        new Date().toISOString()
    });

    if (!result.success) throw new Error(result.error);
    return diagnoseDistributorAccess();
  });
}
// New uploads are private Drive files. Ledger IDs, not Drive IDs, reach the browser.
const IMAGE_FIELDS_ = ['adminImage','distributorReplyImage','paymentScreenshot','renewalScreenshot','pdfPremiumScreenshot'];
const RETENTION_MS_ = 15 * 86400000;
function imageLedger_() {
    const ss=SpreadsheetApp.openById(PORTAL_SPREADSHEET_ID);
  let s=ss.getSheetByName('PortalImageRetention');
  if(!s){s=ss.insertSheet('PortalImageRetention');s.appendRow(['id','fileId','owner','kind','createdAt','deleteAt','deletedAt']);}
  return s;
}
function imageRows_(){const s=imageLedger_();return s.getLastRow()<2?[]:s.getRange(2,1,s.getLastRow()-1,7).getValues();}
function setupPremiumAndCleanup(){
  return withLock_(()=>{
    securityReady_();getSheet_();imageLedger_();pdfDownloadLedger_();sessionLedger_();rateLedger_();transactionLedger_();
    const p=securityProperties_();
    if(!p.getProperty('PORTAL_IMAGE_FOLDER_ID'))p.setProperty('PORTAL_IMAGE_FOLDER_ID',DriveApp.createFolder('Portal private payment images').getId());
    if(!ScriptApp.getProjectTriggers().some(t=>t.getHandlerFunction()==='cleanupPortalImages'))ScriptApp.newTrigger('cleanupPortalImages').timeBased().everyHours(1).create();
    return 'Premium ready; hourly cleanup installed. Existing security settings preserved.';
  });
}
function storePortalImage_(image,owner,kind){
  validImage_(image);owner=email_(owner);if(!['general','payment'].includes(kind))throw new Error('Invalid image purpose.');const folderId=securityProperties_().getProperty('PORTAL_IMAGE_FOLDER_ID');if(!folderId)throw new Error('Run setupPremiumAndCleanup in Apps Script first.');
  const m=image.match(/^data:([^;]+);base64,(.+)$/),id=randomToken_(),now=Date.now(),blob=Utilities.newBlob(Utilities.base64Decode(m[2]),m[1],id+'.'+(m[1]==='image/jpeg'?'jpg':m[1].split('/')[1]));let file;
  try{file=DriveApp.getFolderById(folderId).createFile(blob);}catch(e){throw new Error('Private image storage unavailable.');}
  imageLedger_().appendRow([id,file.getId(),owner,kind,now,now+(kind==='general'?RETENTION_MS_:PAYMENT_PENDING_RETENTION_MS_),'']);return 'managed:'+id;
}
function approveImageRetention_(refs,now){scheduleImageRetention_(refs,now+RETENTION_MS_);}
function managedImage_(data,principal){
  const ref=String(data.ref||'');
  const r=imageRows_().find(r=>'managed:'+r[0]===ref);
  if(!r||r[6]||(Number(r[5])>0&&Number(r[5])<=Date.now()))throw new Error('Image expired or unavailable.');
  if(principal.role==='admin')admin_(principal);
  else if(principal.email!==r[2])throw new Error('Image access denied.');
  const blob=DriveApp.getFileById(r[1]).getBlob();
  return {success:true,imageData:'data:'+blob.getContentType()+';base64,'+Utilities.base64Encode(blob.getBytes())};
}
function cleanupPortalImages(){
  return withLock_(()=>{
    const s=imageLedger_(),start=Date.now();let deleted=0,failed=0;
    // Repair interrupted approval scheduling, including both renewal aliases.
    getDistributors_().forEach(d=>{
      if(stateText_(d.paymentStatus)==='approved'&&Number(d.paymentApprovedAt))approveImageRetention_([d.paymentScreenshot,d.renewalScreenshot],Number(d.paymentApprovedAt));
      if(stateText_(d.pdfPremiumStatus)==='approved'&&Number(d.pdfPremiumApprovedAt))approveImageRetention_([d.pdfPremiumScreenshot],Number(d.pdfPremiumApprovedAt));
    });
    const records=getDistributors_();
    for(const [i,r] of imageRows_().entries()){
      if(Date.now()-start>220000)break;
      if(r[6]||!Number(r[5])||Number(r[5])>Date.now())continue;
      try{
        const response=UrlFetchApp.fetch('https://www.googleapis.com/drive/v3/files/'+encodeURIComponent(r[1]),{method:'delete',headers:{Authorization:'Bearer '+ScriptApp.getOAuthToken()},muteHttpExceptions:true});
        const code=response.getResponseCode();
        if(code!==204&&code!==404){failed++;continue;}
        for(const d of records){const changes={};IMAGE_FIELDS_.forEach(k=>{if(d[k]==='managed:'+r[0])changes[k]='';});if(Object.keys(changes).length)updateDistributor_(d.email,changes);}
        s.getRange(i+2,7).setValue(Date.now());deleted++;
      }catch(e){failed++;}
    }
    cleanupSecurityLedgers_();console.log(JSON.stringify({deleted,failed}));
    if(failed)throw new Error('Some image deletions failed. Check Drive API permissions; next hourly run retries.');
    return {deleted,failed};
  });
}
function maintenanceSettings_(){
  const p=securityProperties_();
  const start=p.getProperty('MAINTENANCE_START')||'',end=p.getProperty('MAINTENANCE_END')||'';
  const now=Date.now(),startMs=start?Date.parse(start):NaN,endMs=end?Date.parse(end):NaN;
  return {enabled:stateText_(p.getProperty('MAINTENANCE_ENABLED'))==='true',start,end,message:p.getProperty('MAINTENANCE_MESSAGE')||'Portal maintenance चल रहा है। कृपया बाद में प्रयास करें।',active:stateText_(p.getProperty('MAINTENANCE_ENABLED'))==='true'&&(!Number.isFinite(startMs)||now>=startMs)&&(!Number.isFinite(endMs)||now<=endMs)};
}
function recoveryKey_(email){return 'recovery:'+sha256_(email_(email));}
function requestPasswordReset_(data){
  const email=email_(data.email),record=record_(email),p=PropertiesService.getScriptProperties();if(!record)throw new Error('If this account exists, a verification code has been sent.');
  throttle_('recovery-v2:'+email,3,120);const otp=String(Math.floor(100000+Math.random()*900000)),key=recoveryKey_(email),now=Date.now();
  PropertiesService.getScriptProperties().setProperty(key,JSON.stringify({email,otpHash:sha256_('otp|'+otp),expires:now+600000,attempts:0,verified:false}));
  try{MailApp.sendEmail({to:email,subject:'OP Printing Hub password reset code',body:'Your password reset OTP is '+otp+'. It expires in 10 minutes. If you did not request this, ignore this email.'});}catch(e){p.deleteProperty(key);throw new Error('OTP email service is not authorized. Run any MailApp function once in Apps Script and deploy a new version.');}
  return {success:true,message:'Verification code sent to your registered email.'};
}
function registrationOtpKey_(email){return 'registration-otp:'+sha256_(email_(email));}
function requestRegistrationOtp_(data){
  const email=email_(data.email),name=text_(data.name,100),officeName=text_(data.officeName,150),mobile=text_(data.mobile,20),p=securityProperties_();
  if(!name||!officeName||!/^[+]?\d[0-9 ()-]{7,18}$/.test(mobile))throw new Error('Office/center name, name and valid mobile number required.');
  if(email===String(p.getProperty('ADMIN_EMAIL')||'').trim().toLowerCase())throw new Error('Invalid registration.');
  if(record_(email))throw new Error('Account already exists. Login to continue or contact admin.');
  throttle_('registration-otp-global',20,3600);throttle_('registration-otp:'+email,3,600);
  const otp=String(Math.floor(100000+Math.random()*900000)),key=registrationOtpKey_(email);
  p.setProperty(key,JSON.stringify({email,name,officeName,mobile,otpHash:sha256_('registration|'+otp),expires:Date.now()+600000,attempts:0,verified:false}));
  try{MailApp.sendEmail({to:email,subject:'OP Printing Hub registration verification',body:'Your registration OTP is '+otp+'. It expires in 10 minutes. If you did not request this, ignore this email.'});}catch(e){p.deleteProperty(key);throw new Error('OTP email service is not authorized. Run authorizeMail() once and deploy a new version.');}
  return {success:true,message:'Registration OTP sent to your email.'};
}
function verifyRegistrationOtp_(data){
  const email=email_(data.email),key=registrationOtpKey_(email),p=securityProperties_(),raw=p.getProperty(key),entry=raw?JSON.parse(raw):null;
  if(!entry||entry.expires<Date.now()||entry.verified)throw new Error('Registration OTP expired. Request a new code.');
  entry.attempts=Number(entry.attempts||0)+1;if(entry.attempts>5){p.deleteProperty(key);throw new Error('Too many attempts. Request a new code.');}
  if(sha256_('registration|'+String(data.otp||''))!==entry.otpHash){p.setProperty(key,JSON.stringify(entry));throw new Error('Invalid registration OTP.');}
  const token=randomToken_();entry.verified=true;entry.verifyHash=sha256_('registration-verified|'+token);entry.expires=Date.now()+900000;p.setProperty(key,JSON.stringify(entry));
  return {success:true,registrationToken:token};
}
// Run once manually as the deployment owner to grant MailApp permission.
function authorizeMail() {
  MailApp.sendEmail(
    Session.getEffectiveUser().getEmail(),
    'OP Printing Hub test',
    'Mail authorization successful.'
  );
}
function verifyPasswordOtp_(data){
  const email=email_(data.email),key=recoveryKey_(email),p=PropertiesService.getScriptProperties(),raw=p.getProperty(key),entry=raw?JSON.parse(raw):null;
  if(!entry||entry.expires<Date.now()||entry.verified)throw new Error('Code expired. Request a new code.');
  entry.attempts=Number(entry.attempts||0)+1;if(entry.attempts>5){p.deleteProperty(key);throw new Error('Too many attempts. Request a new code.');}
  if(sha256_('otp|'+String(data.otp||''))!==entry.otpHash){p.setProperty(key,JSON.stringify(entry));throw new Error('Invalid verification code.');}
  const token=randomToken_();entry.verified=true;entry.resetHash=sha256_('reset|'+token);entry.expires=Date.now()+600000;p.setProperty(key,JSON.stringify(entry));return {success:true,resetToken:token};
}
function resetPassword_(data){
  const email=email_(data.email),password=newPassword_(data.newPass),token=String(data.resetToken||''),key=recoveryKey_(email),p=PropertiesService.getScriptProperties(),raw=p.getProperty(key),entry=raw?JSON.parse(raw):null;
  if(!entry||!entry.verified||entry.expires<Date.now()||!token||sha256_('reset|'+token)!==entry.resetHash)throw new Error('Reset link expired. Start again.');
  const hash=hashPassword_(password),result=withLock_(()=>updateDistributor_(email,{passwordHash:hash,pass:''}));
  if(!result||result.success!==true)throw new Error('Password reset could not be saved. Please try again.');
  p.deleteProperty(key);revokeSessionsForEmail_(email);return {success:true};
}
function revokeSessionsForEmail_(email){const s=sessionLedger_(),rows=rows_(s,8);rows.forEach((r,i)=>{if(String(r[1]).toLowerCase()===email)s.getRange(i+2,7).setValue(Date.now());});}
function maintenanceMessage_(){
  return maintenanceSettings_().message;
}
function maintenanceActive_(){
  const m=maintenanceSettings_();
  if(!m.enabled)return false;
  const now=Date.now(),start=m.start?Date.parse(m.start):NaN,end=m.end?Date.parse(m.end):NaN;
  return (!Number.isFinite(start)||now>=start)&&(!Number.isFinite(end)||now<=end);
}
function setMaintenance_(data,principal){
  admin_(principal);const p=securityProperties_();
  p.setProperties({MAINTENANCE_ENABLED:String(Boolean(data.enabled)),MAINTENANCE_START:text_(data.start||'',40),MAINTENANCE_END:text_(data.end||'',40),MAINTENANCE_MESSAGE:text_(data.message||'Portal maintenance चल रहा है। कृपया बाद में प्रयास करें।',300)});
  return {success:true,maintenance:maintenanceSettings_()};
}
function premiumState_(d){
  if(!d)return 'locked';
  if(stateText_(d.premiumBundleStatus)==='approved'&&Number(d.premiumBundleExpiry)>Date.now())return 'active';
  if(stateText_(d.pdfPremiumStatus)==='approved'&&Number(d.pdfPremiumExpiry)>Date.now())return 'active';
  if(stateText_(d.pdfPremiumStatus)==='pending')return 'pending';
  if(stateText_(d.pdfPremiumStatus)==='rejected')return 'rejected';
  return Number(d.pdfPremiumExpiry)?'expired':'locked';
}
function premiumInfo_(p){return {success:true,downloadQuota:pdfQuota_(p),uploadReady:Boolean(securityProperties_().getProperty('PORTAL_IMAGE_FOLDER_ID')),state:p.role==='admin'?'active':premiumState_(p.record),allowed:p.role==='admin'||(accessState_(p.record)==='active'&&premiumState_(p.record)==='active'),expiry:p.record?Number(p.record.pdfPremiumExpiry)||0:0,amount:159};}
function submitPremium_(data){return withLock_(()=>{
  const p=session_(data);own_(p,data);if(accessState_(p.record)!=='active')throw new Error('Active portal membership required.');const state=premiumState_(p.record);if(['active','pending'].includes(state))throw new Error('Premium is active or already pending.');
  validImage_(data.imageData);const txn=text_(data.txnId,150),requestId=randomToken_();if(!txn)throw new Error('Payment transaction ID required.');const ref=storePortalImage_(data.imageData,p.email,'payment');
  try{claimTransaction_(txn,p.email,'pdf-premium',requestId);const result=updateDistributor_(p.email,{pdfPremiumStatus:'Pending',pdfPremiumAmount:159,pdfPremiumTxnId:txn,pdfPremiumScreenshot:ref,pdfPremiumRequestId:requestId,pdfPremiumRequestedAt:Date.now(),pdfPremiumApprovedAt:0});if(!result.success)throw new Error(result.error);return result;}catch(e){releaseTransaction_(p.email,'pdf-premium',requestId);discardManagedImage_(ref);throw e;}
});}
function reviewPremium_(data){return withLock_(()=>{
  const p=session_(data);admin_(p);const d=record_(email_(data.email));if(!d||premiumState_(d)!=='pending'||String(d.pdfPremiumRequestId)!==String(data.requestId))throw new Error('Request changed or already reviewed. Refresh admin panel.');if(![true,false,'true','false'].includes(data.approved))throw new Error('Invalid decision.');
  const approved=String(data.approved)==='true',now=Date.now(),end=new Date(now);end.setUTCFullYear(end.getUTCFullYear()+1);if(approved&&!d.pdfPremiumScreenshot)throw new Error('Screenshot required.');
  const result=updateDistributor_(d.email,{pdfPremiumStatus:approved?'Approved':'Rejected',pdfPremiumApprovedAt:approved?now:0,pdfPremiumExpiry:approved?end.getTime():Number(d.pdfPremiumExpiry)||0,premiumBundleStatus:approved?'Approved':'Rejected',premiumBundleExpiry:approved?end.getTime():Number(d.premiumBundleExpiry)||0});if(!result.success)throw new Error(result.error);try{scheduleImageRetention_([d.pdfPremiumScreenshot],now+RETENTION_MS_);reviewTransaction_(d.pdfPremiumRequestId,approved?'Approved':'Rejected');}catch(e){console.log('Post-review retention metadata will be repaired by cleanup.');}return result;
});}

// Run manually as owner to diagnose upload configuration. Does not upload/delete files.
function diagnosePremiumUpload(){
  securityReady_();const id=securityProperties_().getProperty('PORTAL_IMAGE_FOLDER_ID');
  const report={folderConfigured:Boolean(id),folderAccessible:false,cleanupInstalled:ScriptApp.getProjectTriggers().some(t=>t.getHandlerFunction()==='cleanupPortalImages')};
  if(id){try{DriveApp.getFolderById(id).getName();report.folderAccessible=true;}catch(e){report.error='Folder unavailable or Drive authorization missing.';}}
  console.log(JSON.stringify(report));return report;
}

// Five authorized PDF Editor downloads per distributor account, across devices.
// No paid top-up and no automatic reset on premium renewal.
const PDF_DOWNLOAD_LIMIT = 5;
function pdfDownloadLedger_(){
  const ss=SpreadsheetApp.openById(PORTAL_SPREADSHEET_ID);let s=ss.getSheetByName('PdfEditorDownloads');
  if(!s){s=ss.insertSheet('PdfEditorDownloads');s.appendRow(['email','requestId','sha256','fileName','createdAt']);}
  return s;
}
function pdfDownloadRows_(){const s=pdfDownloadLedger_();return s.getLastRow()<2?[]:s.getRange(2,1,s.getLastRow()-1,5).getValues();}
function pdfQuota_(p){
  if(p.role==='admin')return {limit:null,used:0,remaining:null};
  const used=pdfDownloadRows_().filter(r=>r[0]===p.email).length;
  return {limit:PDF_DOWNLOAD_LIMIT,used,remaining:Math.max(0,PDF_DOWNLOAD_LIMIT-used)};
}
function authorizePdfDownload_(data){return withLock_(()=>{
  const p=session_(data);
  if(p.role!=='admin'){own_(p,data);if(accessState_(p.record)!=='active'||premiumState_(p.record)!=='active')throw new Error('Active membership and PDF Premium required.');}
  const requestId=String(data.requestId||''),hash=String(data.sha256||''),fileName=text_(data.fileName,180);
  if(!/^[a-zA-Z0-9-]{16,80}$/.test(requestId)||! /^[a-f0-9]{64}$/.test(hash)||!fileName)throw new Error('Invalid download request.');
  if(p.role==='admin')return {success:true,requestId,quota:pdfQuota_(p)};
  const records=pdfDownloadRows_().filter(r=>r[0]===p.email),old=records.find(r=>r[1]===requestId);
  if(old){if(old[2]!==hash||old[3]!==fileName)throw new Error('Download request changed.');return {success:true,requestId,quota:{limit:5,used:records.length,remaining:Math.max(0,5-records.length)},replayed:true};}
  if(records.length>=PDF_DOWNLOAD_LIMIT)throw new Error('PDF_DOWNLOAD_LIMIT: सभी 5 downloads उपयोग हो चुके हैं।');
  pdfDownloadLedger_().appendRow([p.email,requestId,hash,sheetValue_(fileName),Date.now()]);SpreadsheetApp.flush();
  return {success:true,requestId,quota:{limit:5,used:records.length+1,remaining:4-records.length}};
});}


// Security ledgers contain hashes/metadata only. Raw passwords, tokens and transaction IDs are never stored here.
const SESSION_LEDGER_SHEET_='PortalSessions';
const RATE_LEDGER_SHEET_='SecurityRateLimits';
const TXN_LEDGER_SHEET_='PaymentTransactions';
const PAYMENT_PENDING_RETENTION_MS_=90*86400000;
function ledgerSheet_(name,headers){
  const ss=SpreadsheetApp.openById(PORTAL_SPREADSHEET_ID);let s=ss.getSheetByName(name);
  if(!s){s=ss.insertSheet(name);s.appendRow(headers);}return s;
}
function sessionLedger_(){return ledgerSheet_(SESSION_LEDGER_SHEET_,['tokenHash','email','role','version','expires','panelUntil','revokedAt','createdAt']);}
function rateLedger_(){return ledgerSheet_(RATE_LEDGER_SHEET_,['bucketHash','windowStart','count','updatedAt']);}
function transactionLedger_(){return ledgerSheet_(TXN_LEDGER_SHEET_,['txnHash','owner','flow','requestId','createdAt','status','reviewedAt']);}
function rows_(s,width){return s.getLastRow()<2?[]:s.getRange(2,1,s.getLastRow()-1,width).getValues();}
function safeError_(error){
  const m=String(error&&error.message||error||'Request failed.');
  const allowed=['Login required.','Session expired. Please login again.','Invalid email or password.','Admin access required.','Admin panel is locked. Enter your admin password to unlock it.','Incorrect admin password.','Too many attempts. Please try later.','Account already exists. Login to continue or contact admin.','Transaction ID is already used.','Request changed or already reviewed. Refresh the admin panel.','Image expired or unavailable.','Image access denied.','Unknown action.'];
  if(allowed.includes(m)||/^Portal maintenance|चल रहा है|If this account|Verification code|Code expired|Invalid verification|Reset link|Too many attempts|OTP email service|Passwords do not match/.test(m)||/^(Valid email required|Use a password|Text is too long|Invalid |Active |Premium |Renewal |Signup |Payment |Account changed|Distributor not found|PDF_DOWNLOAD_LIMIT)/.test(m))return m.slice(0,220);
  return 'Request failed. Please retry or contact admin.';
}
function transactionHash_(value){return sha256_('txn|'+securityProperties_().getProperty('AUTH_PEPPER')+'|'+String(value||'').trim().toUpperCase());}
function claimTransaction_(txn,owner,flow,requestId){
  const value=text_(txn,150);if(!/^[A-Za-z0-9][A-Za-z0-9 ._\-\/:]{3,149}$/.test(value))throw new Error('Invalid transaction ID.');
  const hash=transactionHash_(value),s=transactionLedger_(),found=rows_(s,7).find(r=>r[0]===hash);
  if(found){if(found[1]===owner&&found[2]===flow&&found[3]===requestId)return;throw new Error('Transaction ID is already used.');}
  // Backward-compatible duplicate check before the ledger migration has been run.
  for(const d of getDistributors_())for(const key of ['paymentTxnId','renewalTxnId','pdfPremiumTxnId']){
    const old=String(d[key]||'').trim();if(old&&transactionHash_(old)===hash)throw new Error('Transaction ID is already used.');
  }
  s.appendRow([hash,owner,flow,requestId,Date.now(),'Pending','']);SpreadsheetApp.flush();
}
function reviewTransaction_(requestId,status){
  const s=transactionLedger_(),all=rows_(s,7);for(let i=0;i<all.length;i++)if(all[i][3]===requestId){s.getRange(i+2,6,1,2).setValues([[status,Date.now()]]);return;}
}
function releaseTransaction_(owner,flow,requestId){
  const s=transactionLedger_(),all=rows_(s,7);for(let i=all.length-1;i>=0;i--)if(all[i][1]===owner&&all[i][2]===flow&&all[i][3]===requestId&&stateText_(all[i][5])==='pending'){s.deleteRow(i+2);return;}
}
function rebindTransaction_(txn,owner,requestId){
  const hash=transactionHash_(txn),s=transactionLedger_(),all=rows_(s,7);for(let i=0;i<all.length;i++)if(all[i][0]===hash&&all[i][1]===owner){s.getRange(i+2,4).setValue(requestId);return;}
}
function updateSessionLedger_(tokenHash,changes){
  const s=sessionLedger_(),all=rows_(s,8),i=all.findIndex(r=>r[0]===tokenHash);if(i<0)return false;
  const map={email:2,role:3,version:4,expires:5,panelUntil:6,revokedAt:7};Object.keys(changes).forEach(k=>{if(map[k])s.getRange(i+2,map[k]).setValue(changes[k]);});return true;
}
function cleanupSecurityLedgers_(){
  const now=Date.now(),sessions=sessionLedger_(),sr=rows_(sessions,8);for(let i=sr.length-1;i>=0;i--)if(Number(sr[i][4])<now-86400000||Number(sr[i][6]))sessions.deleteRow(i+2);
  const rates=rateLedger_(),rr=rows_(rates,4);for(let i=rr.length-1;i>=0;i--)if(Number(rr[i][3])<now-7*86400000)rates.deleteRow(i+2);
}
function discardManagedImage_(ref){scheduleImageRetention_([ref],Date.now());}
function updateAdminMessage_(email,message,imageRef){
  try{return withLock_(()=>{if(!record_(email))throw new Error('Distributor not found.');const result=updateDistributor_(email,{adminMessage:message,adminImage:imageRef});if(!result.success)throw new Error(result.error);return result;});}catch(e){if(imageRef)discardManagedImage_(imageRef);throw e;}
}
function scheduleImageRetention_(refs,deleteAt){
  const wanted={};refs.filter(Boolean).forEach(x=>wanted[String(x)]=true);const s=imageLedger_();imageRows_().forEach((r,i)=>{
    if(!r[6]&&wanted['managed:'+r[0]])s.getRange(i+2,6).setValue(deleteAt);
  });
}
function auditSecurityData(){
  securityReady_();const sheet=getSheet_(),emailColumn=getHeaderMap_(sheet).email,raw=sheet.getLastRow()<2?[]:sheet.getRange(2,emailColumn,sheet.getLastRow()-1,1).getValues(),byEmail={},duplicateEmailRows=[];raw.forEach((r,i)=>{const key=String(r[0]||'').trim().toLowerCase();if(!key)return;if(byEmail[key]!==undefined)duplicateEmailRows.push([byEmail[key],i+2]);else byEmail[key]=i+2;});const records=getDistributors_();
  const txnSeen={},duplicateTransactionKinds=[];records.forEach(d=>[['paymentTxnId','membership'],['renewalTxnId','renewal'],['pdfPremiumTxnId','pdf-premium']].forEach(pair=>{const value=String(d[pair[0]]||'').trim();if(!value||value==='Admin Assignment')return;const hash=transactionHash_(value);if(txnSeen[hash]&&txnSeen[hash]!==d.email)duplicateTransactionKinds.push(pair[1]);else txnSeen[hash]=d.email;}));
  const report={success:true,records:records.length,duplicateEmailRows,duplicateTransactionCount:duplicateTransactionKinds.length,duplicateTransactionKinds};console.log(JSON.stringify(report));return report;
}
function migrateSecuritySchema(){
  securityReady_();return withLock_(()=>{
    const audit=auditSecurityData();if(audit.duplicateEmailRows.length)throw new Error('Duplicate account rows found. Resolve the rows reported by auditSecurityData before migration.');
    getSheet_();sessionLedger_();rateLedger_();transactionLedger_();imageLedger_();pdfDownloadLedger_();
    let seeded=0;const s=transactionLedger_(),known={};rows_(s,7).forEach(r=>known[r[0]]=true);
    getDistributors_().forEach(d=>{
      if(!d.paymentRequestId&&stateText_(d.paymentStatus)==='pending')updateDistributor_(d.email,{paymentRequestId:randomToken_(),paymentRequestedAt:Number(d.renewalRequestedAt)||Date.now()});
      [['paymentTxnId','membership'],['renewalTxnId','renewal'],['pdfPremiumTxnId','pdf-premium']].forEach(pair=>{
        const txn=String(d[pair[0]]||'').trim();if(!txn||txn==='Admin Assignment')return;const hash=transactionHash_(txn);if(known[hash])return;
        const requestId=pair[1]==='pdf-premium'?String(d.pdfPremiumRequestId||'legacy:'+d.id+':pdf'):String(d.paymentRequestId||'legacy:'+d.id+':'+pair[1]);
        s.appendRow([hash,d.email,pair[1],requestId,Number(d.paymentRequestedAt)||Number(d.renewalRequestedAt)||Number(d.assignedTimestamp)||Date.now(),stateText_(pair[1]==='pdf-premium'?d.pdfPremiumStatus:d.paymentStatus)||'legacy',Number(d.pdfPremiumApprovedAt)||Number(d.paymentApprovedAt)||'']);known[hash]=true;seeded++;
      });
    });SpreadsheetApp.flush();return {success:true,seeded};
  });
}
