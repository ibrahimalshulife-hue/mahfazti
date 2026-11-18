from flask import Flask, request, session, redirect, jsonify, Response
app = Flask(__name__)
app.secret_key='mahfazti2026'
users={'777111':{'name':'Ahmed','pass':'1234','bal':10000,'hist':[]}}

MANIFEST={"name":"Mahfazti - محفظتي","short_name":"محفظتي","start_url":"/","display":"standalone","background_color":"#FFB800","theme_color":"#FFB800","icons":[{"src":"/icon.png","sizes":"512x512","type":"image/png"}]}
@app.route('/manifest.json')
def man(): return jsonify(MANIFEST)
@app.route('/sw.js')
def sw():
 return Response("self.addEventListener('fetch',e=>{e.respondWith(fetch(e.request).catch(()=>caches.match(e.request)))})", mimetype='application/javascript')
@app.route('/icon.png')
def icon():
 # أيقونة صفراء بسيطة
 import base64
 # 1x1 png اصفر سيتم تكبيره من المتصفح
 return redirect("https://cdn-icons-png.flaticon.com/512/3135/3135679.png")

CSS="""
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="manifest" href="/manifest.json"><meta name="theme-color" content="#FFB800">
<meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-capable" content="yes">
<style>*{box-sizing:border-box;font-family:Arial}body{margin:0;background:#F5F5F5;padding-bottom:85px}.top{background:#FFB800;padding:18px 15px 70px;border-radius:0 0 25px 25px}.top-row{display:flex;justify-content:space-between;color:#000;font-weight:bold}.card{background:#fff;margin:-45px 15px 15px;padding:20px;border-radius:20px;box-shadow:0 4px 15px #ddd;text-align:center}.card h1{font-size:30px;margin:5px}.btns{display:flex;gap:10px}.btns a{flex:1;padding:13px;border-radius:12px;text-align:center;text-decoration:none;font-weight:bold;color:#000}.y{background:#FFB800}.g{background:#F2F2F2}.box{background:#fff;margin:15px;padding:15px;border-radius:20px}.grid{display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:10px;text-align:center}.item{background:#FFF8E1;padding:12px 5px;border-radius:15px;text-decoration:none;color:#000}.item span{font-size:24px;display:block}.item b{font-size:12px}input{width:100%;padding:13px;margin:8px 0;border:1px solid #ddd;border-radius:12px;text-align:center;font-size:16px}button,.send{background:#FFB800;border:0;width:100%;padding:14px;border-radius:12px;font-weight:bold;font-size:16px}select{width:100%;padding:13px;margin:8px 0;border-radius:12px}.bottom{position:fixed;bottom:0;left:0;right:0;background:#fff;display:flex;justify-content:space-around;padding:12px 0;box-shadow:0 -2px 10px #ddd}.bottom a{text-decoration:none;color:#000;text-align:center;font-size:13px}.row{display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid #eee}</style>
<script>if('serviceWorker' in navigator){navigator.serviceWorker.register('/sw.js')}</script>
"""
def header(t):
 return f"<div class='top'><div class='top-row'><div><a href='/' style='text-decoration:none;color:#000'>⬅ رجوع</a></div><div>{t}</div><div>🔔</div></div></div>"
def bottom():
 return "<div class='bottom'><a href='/'>🏠<br>الرئيسية</a><a href='/tahwil'>💸<br>تحويل</a><a href='/shahn'>📱<br>شحن</a><a href='/hisabi'>👤<br>حسابي</a></div>"

@app.route('/')
def home():
 if 'raq' not in session: return CSS+f"<div class='top'><div class='top-row'><div>👤</div><div>محفظتي</div><div>🔔</div></div></div><div class='card'><h2>أهلا بك في محفظتي</h2><p>مثل جيب تماما</p><div class='btns'><a class='y' href='/jadid'>حساب جديد</a><a class='g' href='/dukhol'>دخول</a></div></div>"+bottom()
 u=users[session['raq']]
 hist="".join([f"<div class='row'><span>{h}</span></div>" for h in u['hist'][-5:]]) or "<p style='text-align:center;color:#999'>لا توجد عمليات</p>"
 return CSS+f"""
 <div class='top'><div class='top-row'><div>👤 {u['name']}</div><div>محفظتي</div><div>🔔</div></div></div>
 <div class='card'><small>الرصيد المتاح</small><h1>{u['bal']} ريال</h1><p>{u['name']} - {session['raq']}</p><div class='btns'><a class='y' href='/tahwil'>تحويل ⬆️</a><a class='g' href='/shahn'>شحن +</a></div></div>
 <div class='box'><h3>خدماتنا</h3><div class='grid'>
 <a class='item' href='/tahwil'><span>💸</span><b>تحويل</b></a>
 <a class='item' href='/shahn'><span>📱</span><b>شحن رصيد</b></a>
 <a class='item' href='/fawateer'><span>🧾</span><b>فواتير</b></a>
 <a class='item' href='/shahn'><span>🌐</span><b>انترنت</b></a>
 <a class='item' href='/fawateer'><span>💡</span><b>كهرباء</b></a>
 <a class='item' href='/fawateer'><span>💧</span><b>ماء</b></a>
 <a class='item' href='/matager'><span>🛒</span><b>متاجر</b></a>
 <a class='item' href='/hisabi'><span>⚙️</span><b>حسابي</b></a>
 </div></div>
 <div class='box'><h3>آخر العمليات</h3>{hist}</div>
 """+bottom()

@app.route('/jadid',methods=['GET','POST'])
def jadid():
 if request.method=='POST':
  raq=request.form['raq']; users[raq]={'name':request.form['ism'],'pass':request.form['sir'],'bal':1000,'hist':[]}; session['raq']=raq; return redirect('/')
 return CSS+header('حساب جديد')+"<div class='box'><form method='post'><input name='ism' placeholder='الاسم الكامل' required><input name='raq' placeholder='رقم الجوال' required><input name='sir' type='password' placeholder='كلمة السر' required><button>إنشاء حساب - هدية 1000 ريال</button></form></div>"+bottom()
@app.route('/dukhol',methods=['GET','POST'])
def dukhol():
 if request.method=='POST':
  raq=request.form['raq']
  if raq in users and users[raq]['pass']==request.form['sir']: session['raq']=raq; return redirect('/')
  return "رقم او كلمة سر غلط <a href='/dukhol'>رجوع</a>"
 return CSS+header('دخول')+"<div class='box'><form method='post'><input name='raq' placeholder='رقم الجوال'><input name='sir' type='password' placeholder='كلمة السر'><button>دخول</button></form></div>"+bottom()
@app.route('/tahwil',methods=['GET','POST'])
def tahwil():
 if 'raq' not in session: return redirect('/dukhol')
 if request.method=='POST':
  to=request.form['to']; m=int(request.form['m']); me=users[session['raq']]
  if to in users and me['bal']>=m: me['bal']-=m; users[to]['bal']+=m; me['hist'].append(f"تحويل {m} الى {to}"); users[to]['hist'].append(f"وصلك {m} من {session['raq']}"); return redirect('/')
  return "رصيد ما يكفي او الرقم غلط <a href='/'>رجوع</a>"
 return CSS+header('تحويل')+"<div class='box'><form method='post'><input name='to' placeholder='رقم المستلم'><input name='m' type='number' placeholder='المبلغ'><button>تحويل الان</button></form></div>"+bottom()
@app.route('/shahn',methods=['GET','POST'])
def shahn():
 if 'raq' not in session: return redirect('/dukhol')
 if request.method=='POST':
  m=int(request.form['m']); net=request.form['net']; me=users[session['raq']]
  if me['bal']>=m: me['bal']-=m; me['hist'].append(f"شحن {net} - {m} ريال"); return redirect('/')
  return "رصيد ما يكفي"
 return CSS+header('شحن رصيد')+"<div class='box'><form method='post'><select name='net'><option>يمن موبايل</option><option>سبأفون</option><option>يو YOU</option><option>واي Y</option></select><input name='phone' placeholder='رقم الجوال'><input name='m' type='number' placeholder='المبلغ'><button>شحن الان</button></form></div>"+bottom()
@app.route('/fawateer',methods=['GET','POST'])
def fawateer():
 if 'raq' not in session: return redirect('/dukhol')
 if request.method=='POST':
  m=int(request.form['m']); me=users[session['raq']]
  if me['bal']>=m: me['bal']-=m; me['hist'].append(f"دفع فاتورة {request.form['type']} - {m}"); return redirect('/')
  return "رصيد ما يكفي"
 return CSS+header('دفع فواتير')+"<div class='box'><form method='post'><select name='type'><option>كهرباء</option><option>ماء</option><option>انترنت ADSL</option><option>تلفون ثابت</option></select><input name='num' placeholder='رقم الفاتورة / الحساب'><input name='m' type='number' placeholder='المبلغ'><button>دفع الان</button></form></div>"+bottom()
@app.route('/matager')
def matager(): return CSS+header('متاجر')+"<div class='box'><h3>متاجر قريبا</h3><p>ادفع في المتاجر برمز QR</p></div>"+bottom()
@app.route('/hisabi')
def hisabi():
 if 'raq' not in session: return redirect('/dukhol')
 u=users[session['raq']]; return CSS+header('حسابي')+f"<div class='box'><p>الاسم: {u['name']}</p><p>الرقم: {session['raq']}</p><p>الرصيد: {u['bal']}</p><a href='/logout'>خروج</a></div>"+bottom()
@app.route('/logout')
def logout(): session.clear(); return redirect('/')
if __name__=='__main__': print("Shaghal 5001"); app.run(host='0.0.0.0',port=5001)
