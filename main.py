from flask import Flask, render_template_string, request
from datetime import datetime

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Automatika | Bot de Citas por WhatsApp - Nunca Pierdas un Cliente</title>
  <meta name="description" content="Convierte conversaciones en citas confirmadas. Bot inteligente para WhatsApp que agenda 24/7, reduce ausencias y libera tu tiempo." />
  <style>
    :root {
      --bg:#0a0e1a;
      --surface:#0f1420;
      --card:#141824;
      --text:#f1f5f9;
      --muted:#94a3b8;
      --dim:#64748b;
      --brand:#10b981;
      --brand-light:#34d399;
      --accent:#f59e0b;
      --warning:#ef4444;
      --shadow: 0 20px 60px rgba(0,0,0,.4);
      --glow: 0 0 40px rgba(16,185,129,.15);
      --radius: 20px;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', sans-serif;
      background: radial-gradient(ellipse 1400px 800px at 10% -20%, rgba(16,185,129,.08) 0%, transparent 50%),
                  radial-gradient(ellipse 1200px 700px at 90% 20%, rgba(6,78,59,.12) 0%, transparent 60%),
                  linear-gradient(180deg, #0a0e1a 0%, #050810 100%);
      color: var(--text);
      line-height: 1.6;
      overflow-x: hidden;
      -webkit-font-smoothing: antialiased;
    }
    .container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }
    header {
      padding: 20px 0;
      backdrop-filter: blur(12px);
      border-bottom: 1px solid rgba(255,255,255,.05);
      position: sticky; top: 0; z-index: 100;
      background: rgba(10,14,26,.85);
    }
    .nav { display: flex; align-items: center; justify-content: space-between; }
    .brand {
      font-weight: 900; font-size: 24px; letter-spacing: -0.5px;
      background: linear-gradient(135deg, var(--brand) 0%, var(--brand-light) 100%);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    }
    .nav-cta {
      display: inline-flex; align-items: center; gap: 8px; padding: 10px 20px;
      background: var(--brand); color: #022c22; font-weight: 700; border-radius: 12px;
      text-decoration: none; font-size: 14px; transition: all .3s ease;
    }
    .nav-cta:hover { background: var(--brand-light); transform: translateY(-2px); box-shadow: 0 8px 25px rgba(16,185,129,.3); }
    .hero { padding: 80px 0 60px; }
    .hero-grid { display: grid; grid-template-columns: 1.2fr 1fr; gap: 60px; align-items: center; }
    .urgency {
      display: inline-flex; align-items: center; gap: 8px;
      background: linear-gradient(135deg, rgba(239,68,68,.15) 0%, rgba(239,68,68,.05) 100%);
      border: 1px solid rgba(239,68,68,.3); padding: 8px 16px; border-radius: 50px;
      font-size: 13px; font-weight: 600; color: #fca5a5; margin-bottom: 24px; animation: pulse 2s ease-in-out infinite;
    }
    @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: .7; } }
    .dot { width: 8px; height: 8px; background: var(--warning); border-radius: 50%; animation: blink 1.5s ease infinite; }
    @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: .3; } }
    h1 { font-size: 56px; line-height: 1.1; font-weight: 900; margin-bottom: 20px; letter-spacing: -1.5px; }
    .highlight {
      color: var(--brand-light);
      text-decoration: underline; text-decoration-color: var(--brand);
      text-decoration-thickness: 3px; text-underline-offset: 4px;
    }
    .subtitle { font-size: 20px; color: var(--muted); margin-bottom: 32px; line-height: 1.7; }
    .cta-group { display: flex; gap: 16px; margin-bottom: 36px; flex-wrap: wrap; }
    .btn-primary {
      display: inline-flex; align-items: center; gap: 10px; padding: 18px 32px;
      background: linear-gradient(135deg, var(--brand) 0%, #059669 100%);
      color: #022c22; font-weight: 800; font-size: 17px; border-radius: 14px;
      text-decoration: none; transition: all .3s ease; box-shadow: 0 8px 30px rgba(16,185,129,.25);
    }
    .btn-primary:hover { transform: translateY(-3px); box-shadow: 0 12px 40px rgba(16,185,129,.4); }
    .btn-secondary {
      display: inline-flex; align-items: center; gap: 10px; padding: 18px 32px;
      background: transparent; color: var(--text); font-weight: 700; font-size: 17px; border-radius: 14px;
      text-decoration: none; border: 2px solid rgba(255,255,255,.15); transition: all .3s ease;
    }
    .btn-secondary:hover { border-color: var(--brand); background: rgba(16,185,129,.05); transform: translateY(-2px); }
    .social-proof { display: flex; gap: 16px; flex-wrap: wrap; }
    .stat {
      display: flex; align-items: center; gap: 8px; padding: 10px 16px;
      background: rgba(16,185,129,.08); border: 1px solid rgba(16,185,129,.2);
      border-radius: 12px; font-size: 13px; font-weight: 600; color: var(--brand-light);
    }
    .demo-container { position: relative; perspective: 1000px; }
    .phone {
      aspect-ratio: 9/19.5; max-width: 360px; margin: 0 auto; border-radius: 42px; border: 12px solid #0d1117;
      background: #000; box-shadow: var(--shadow), var(--glow); overflow: hidden; transform: rotateY(-8deg) rotateX(2deg);
      transition: transform .5s ease;
    }
    .phone:hover { transform: rotateY(0deg) rotateX(0deg); }
    .phone::before {
      content: ''; position: absolute; top: 0; left: 50%; transform: translateX(-50%);
      width: 120px; height: 28px; background: #000; border-radius: 0 0 20px 20px; z-index: 10;
    }
    .screen {
      height: 100%; background: linear-gradient(180deg, #0f1419 0%, #0a0e13 100%);
      padding: 40px 16px 16px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px;
    }
    .whatsapp-header {
      display: flex; align-items: center; gap: 12px; padding: 12px 16px;
      background: #1f2937; margin: -40px -16px 16px; padding-top: 48px;
    }
    .avatar {
      width: 40px; height: 40px; border-radius: 50%;
      background: linear-gradient(135deg, var(--brand) 0%, #059669 100%);
      display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 18px; color: #022c22;
    }
    .contact-name { font-weight: 700; font-size: 15px; }
    .online { font-size: 12px; color: var(--muted); }
    .message {
      max-width: 80%; padding: 12px 14px; border-radius: 12px; font-size: 14px; line-height: 1.5; animation: slideIn .4s ease;
    }
    @keyframes slideIn { from { opacity: 0; transform: translateY(10px);} to { opacity: 1; transform: translateY(0);} }
    .message-in  { background: #1f2937; align-self: flex-start; border-bottom-left-radius: 4px; }
    .message-out { background: var(--brand); color: #022c22; align-self: flex-end; border-bottom-right: 4px; font-weight: 500; }
    .section { padding: 80px 0; }
    .section-header { text-align: center; max-width: 700px; margin: 0 auto 60px; }
    .kicker {
      display: inline-block; color: var(--brand-light); font-weight: 800; font-size: 13px; letter-spacing: 2px;
      text-transform: uppercase; margin-bottom: 16px;
    }
    h2 { font-size: 42px; font-weight: 900; margin-bottom: 16px; letter-spacing: -1px; }
    .section-subtitle { font-size: 18px; color: var(--muted); }
    .benefits-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
    .benefit-card {
      background: linear-gradient(135deg, var(--card) 0%, var(--surface) 100%);
      border: 1px solid rgba(255,255,255,.06); border-radius: var(--radius); padding: 32px; transition: all .3s ease; position: relative;
    }
    .benefit-card::before {
      content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
      background: linear-gradient(90deg, var(--brand) 0%, var(--brand-light) 100%);
      transform: scaleX(0); transition: transform .3s ease;
    }
    .benefit-card:hover::before { transform: scaleX(1); }
    .benefit-card:hover { transform: translateY(-8px); box-shadow: var(--shadow); border-color: rgba(16,185,129,.3); }
    .benefit-icon { font-size: 48px; margin-bottom: 20px; }
    .benefit-card h3 { font-size: 20px; font-weight: 800; margin-bottom: 12px; }
    .benefit-card p { color: var(--muted); font-size: 15px; line-height: 1.7; }
    .problem-solution {
      background: linear-gradient(135deg, var(--card) 0%, var(--surface) 100%);
      border: 1px solid rgba(255,255,255,.06); border-radius: var(--radius); padding: 48px; margin: 80px 0;
    }
    .ps-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 48px; }
    .problem { border-left: 4px solid var(--warning); padding-left: 24px; }
    .problem h3 { color: #fca5a5; font-size: 24px; margin-bottom: 16px; font-weight: 800; }
    .problem ul { list-style: none; }
    .problem li {
      color: var(--muted); margin-bottom: 12px; padding-left: 28px; position: relative; font-size: 15px;
    }
    .problem li::before { content: '✗'; position: absolute; left: 0; color: var(--warning); font-weight: 900; }
    .solution { border-left: 4px solid var(--brand); padding-left: 24px; }
    .solution h3 { color: var(--brand-light); font-size: 24px; margin-bottom: 16px; font-weight: 800; }
    .solution ul { list-style: none; }
    .solution li {
      color: var(--muted); margin-bottom: 12px; padding-left: 28px; position: relative; font-size: 15px;
    }
    .solution li::before { content: '✓'; position: absolute; left: 0; color: var(--brand); font-weight: 900; }
    .steps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px; position: relative; }
    .step { text-align: center; }
    .step-number {
      width: 80px; height: 80px; margin: 0 auto 24px; border-radius: 50%;
      background: linear-gradient(135deg, var(--brand) 0%, #059669 100%);
      display: flex; align-items: center; justify-content: center; font-size: 32px; font-weight: 900; color: #022c22;
      box-shadow: 0 8px 30px rgba(16,185,129,.3);
    }
    .step h3 { font-size: 22px; margin-bottom: 12px; font-weight: 800; }
    .step p { color: var(--muted); font-size: 15px; line-height: 1.7; }
    .faq-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; max-width: 1000px; margin: 0 auto; }
    .faq-item { background: var(--card); border: 1px solid rgba(255,255,255,.06); border-radius: 16px; padding: 24px; }
    .faq-item h3 { font-size: 18px; font-weight: 800; margin-bottom: 12px; }
    .faq-item p { color: var(--muted); font-size: 15px; line-height: 1.7; }
    .cta-final {
      background: linear-gradient(135deg, rgba(16,185,129,.15) 0%, rgba(6,78,59,.1) 100%);
      border: 2px solid rgba(16,185,129,.3); border-radius: var(--radius);
      padding: 60px 48px; text-align: center; margin: 60px 0;
    }
    .cta-final h2 { font-size: 38px; margin-bottom: 16px; }
    .cta-final p { font-size: 18px; color: var(--muted); margin-bottom: 32px; }
    .guarantee { display: inline-flex; align-items: center; gap: 8px; margin-top: 20px; color: var(--brand-light); font-size: 14px; font-weight: 600; }
    footer { padding: 40px 0; border-top: 1px solid rgba(255,255,255,.05); }
    .footer-content { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 24px; }
    .footer-badges { display: flex; gap: 12px; flex-wrap: wrap; }
    .badge {
      padding: 8px 14px; background: rgba(255,255,255,.03); border: 1px solid rgba(255,255,255,.08);
      border-radius: 8px; font-size: 12px; color: var(--dim); font-weight: 600;
    }
    .footer-contact a { color: var(--brand-light); text-decoration: none; font-weight: 600; }
    @media (max-width: 968px) {
      h1 { font-size: 36px; }
      .hero-grid { grid-template-columns: 1fr; }
      .benefits-grid { grid-template-columns: 1fr; }
      .steps { grid-template-columns: 1fr; }
      .ps-grid { grid-template-columns: 1fr; }
      .faq-grid { grid-template-columns: 1fr; }
      .phone { max-width: 300px; }
    }
  </style>
</head>
<body>
  <header>
    <div class="container">
      <nav class="nav">
        <div class="brand">AUTOMATIKA</div>
        <a class="nav-cta" href="https://wa.me/{{ phone_e164 }}?text={{ cta_text|urlencode }}">💬 Agenda tu Demo</a>
      </nav>
    </div>
  </header>

  <main>
    <section class="hero">
      <div class="container">
        <div class="hero-grid">
          <div>
            <div class="urgency">
              <span class="dot"></span>
              ¿Perdiendo clientes mientras duermes?
            </div>
            <h1>Convierte leads en <span class="highlight">citas confirmadas</span> automáticamente</h1>
            <p class="subtitle">Tu bot inteligente de WhatsApp que agenda 24/7, confirma citas y reduce ausencias. Mientras tu competencia pierde oportunidades, tú cierras más ventas.</p>

            <div class="cta-group">
              <a class="btn-primary" href="https://wa.me/{{ phone_e164 }}?text={{ cta_text|urlencode }}">🚀 Quiero mi Demo Gratis</a>
              <a class="btn-secondary" href="#como-funciona">Ver cómo funciona →</a>
            </div>

            <div class="social-proof">
              <div class="stat">⚡ Respuesta en &lt;1 min</div>
              <div class="stat">📈 +40% conversión</div>
              <div class="stat">💰 -25% ausencias</div>
            </div>
          </div>

          <div class="demo-container">
            <div class="phone">
              <div class="screen">
                <div class="whatsapp-header">
                  <div class="avatar">A</div>
                  <div>
                    <div class="contact-name">Automatika Bot</div>
                    <div class="online">En línea</div>
                  </div>
                </div>
                <div class="message message-in">👋 ¡Hola! Soy tu asistente de citas. ¿Te gustaría agendar una consulta?</div>
                <div class="message message-out">Sí, para mañana si es posible</div>
                <div class="message message-in">Perfecto. Tengo disponibilidad:<br>• 15:30<br>• 17:00<br>¿Cuál prefieres?</div>
                <div class="message message-out">17:00 está bien</div>
                <div class="message message-in">✅ ¡Listo! Te agendé para <strong>mañana 17:00</strong><br><br>Te recordaré 2 horas antes. ¿Necesitas algo más?</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-header">
          <span class="kicker">El problema que resolvemos</span>
          <h2>¿Te suena familiar?</h2>
        </div>

        <div class="problem-solution">
          <div class="ps-grid">
            <div class="problem">
              <h3>❌ Sin automatización</h3>
              <ul>
                <li>Leads que escriben fuera de horario y nunca responden</li>
                <li>Clientes que olvidan su cita y no llegan</li>
                <li>Tu equipo contestando lo mismo 100 veces al día</li>
                <li>Oportunidades perdidas cada fin de semana</li>
                <li>Agenda desorganizada y doble reservas</li>
              </ul>
            </div>

            <div class="solution">
              <h3>✅ Con Automatika</h3>
              <ul>
                <li>Respuesta inmediata 24/7, todos los días del año</li>
                <li>Recordatorios automáticos que reducen ausencias</li>
                <li>Bot que califica y agenda sin intervención humana</li>
                <li>Captura leads mientras tu competencia duerme</li>
                <li>Integración directa con tu calendario</li>
              </ul>
            </div>
          </div>
        </div>

      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-header">
          <span class="kicker">Beneficios reales</span>
          <h2>¿Qué ganas con Automatika?</h2>
          <p class="section-subtitle">Resultados medibles desde el primer día</p>
        </div>

        <div class="benefits-grid">
          <div class="benefit-card">
            <div class="benefit-icon">💰</div>
            <h3>Más ingresos</h3>
            <p>Convierte hasta 40% más conversaciones en citas confirmadas. Cada lead que llega es atendido inmediatamente.</p>
          </div>

          <div class="benefit-card">
            <div class="benefit-icon">⏰</div>
            <h3>Ahorra tiempo</h3>
            <p>Libera a tu equipo de tareas repetitivas. Enfócate en atender, no en agendar.</p>
          </div>

          <div class="benefit-card">
            <div class="benefit-icon">📉</div>
            <h3>Menos ausencias</h3>
            <p>Recordatorios automáticos reducen hasta 25% las citas perdidas. Tu agenda se mantiene llena.</p>
          </div>

          <div class="benefit-card">
            <div class="benefit-icon">🌙</div>
            <h3>Vende 24/7</h3>
            <p>Captura leads de madrugada, fines de semana y feriados. Nunca pierdas una oportunidad.</p>
          </div>

          <div class="benefit-card">
            <div class="benefit-icon">🎯</div>
            <h3>Calificación inteligente</h3>
            <p>El bot identifica clientes serios y prioriza tu tiempo en lo que realmente vale.</p>
          </div>

          <div class="benefit-card">
            <div class="benefit-icon">📊</div>
            <h3>Reportes claros</h3>
            <p>Ve en tiempo real cuántas citas agendas, tasa de conversión y mejoras en tu negocio.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section" id="como-funciona">
      <div class="container">
        <div class="section-header">
          <span class="kicker">Simple y efectivo</span>
          <h2>¿Cómo funciona?</h2>
          <p class="section-subtitle">En 3 pasos tu negocio está automatizado</p>
        </div>

        <div class="steps">
          <div class="step">
            <div class="step-number">1</div>
            <h3>Cliente escribe</h3>
            <p>Tu cliente envía un mensaje a WhatsApp y el bot responde instantáneamente, sin importar la hora.</p>
          </div>

          <div class="step">
            <div class="step-number">2</div>
            <h3>Bot agenda</h3>
            <p>Ofrece horarios disponibles, captura datos y confirma la cita en tu calendario automáticamente.</p>
          </div>

          <div class="step">
            <div class="step-number">3</div>
            <h3>Recordatorios</h3>
            <p>Envía confirmaciones y recordatorios antes de la cita para minimizar ausencias.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-header">
          <span class="kicker">Preguntas frecuentes</span>
          <h2>Todo lo que necesitas saber</h2>
        </div>

        <div class="faq-grid">
          <div class="faq-item">
            <h3>¿Necesito tener un CRM o sistema complejo?</h3>
            <p>No. Empezamos solo con WhatsApp y Google Calendar. Las integraciones avanzadas son opcionales.</p>
          </div>

          <div class="faq-item">
            <h3>¿Puedo usar mi número actual de WhatsApp?</h3>
            <p>Sí. Trabajamos con tu número existente o configuramos uno nuevo exclusivo para agendamiento.</p>
          </div>

          <div class="faq-item">
            <h3>¿Cuánto tiempo tarda la implementación?</h3>
            <p>El piloto está listo en días. Ajustamos según tus reglas de negocio y preferencias.</p>
          </div>

          <div class="faq-item">
            <h3>¿El bot puede manejar casos especiales?</h3>
            <p>Sí. Lo entrenamos con tus políticas, horarios especiales, tipos de servicio y preguntas frecuentes.</p>
          </div>

          <div class="faq-item">
            <h3>¿Qué pasa si el cliente tiene una pregunta compleja?</h3>
            <p>El bot detecta cuando debe transferir a un humano y te notifica inmediatamente.</p>
          </div>

          <div class="faq-item">
            <h3>¿Es seguro para mis datos y los de mis clientes?</h3>
            <p>Totalmente. Cumplimos estándares de seguridad y privacidad. Tus datos están encriptados.</p>
          </div>
        </div>

        <div class="cta-final">
          <h2>¿Listo para capturar más leads y cerrar más citas?</h2>
          <p>Agenda una demo gratuita y te mostramos cómo Automatika puede transformar tu proceso de ventas en días, no meses.</p>
          <a class="btn-primary" href="https://wa.me/{{ phone_e164 }}?text={{ cta_text|urlencode }}" style="font-size: 18px; padding: 20px 40px;">💬 Agendar mi Demo Gratis</a>
          <div class="guarantee">✓ Sin compromiso · ✓ Configuración en días · ✓ Soporte continuo</div>
        </div>
      </div>
    </section>
  </main>

  <footer>
    <div class="container">
      <div class="footer-content">
        <div class="footer-badges">
          <span class="badge">Respuesta &lt;1 min</span>
          <span class="badge">Implementación express</span>
          <span class="badge">Data segura</span>
        </div>
        <div class="footer-contact">
          © {{ year }} Automatika · <a href="mailto:{{ email }}">Contacto</a>
        </div>
      </div>
    </div>
  </footer>

  <script>
    // Nudge: si no interactúa en 12s, hace scroll a "Cómo funciona"
    setTimeout(() => {
      const el = document.getElementById('como-funciona');
      if (el && !sessionStorage.getItem('nudge')) {
        el.scrollIntoView({ behavior: 'smooth' });
        sessionStorage.setItem('nudge','1');
      }
    }, 12000);
  </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(
        TEMPLATE,
        phone_e164=(request.args.get("phone") or "593999999999"),
        cta_text="Hola, quiero una demo del bot de citas de Automatika",
        year=datetime.now().year,
        email="hola@automatika.example",
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
