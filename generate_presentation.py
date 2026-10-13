import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 widescreen
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette - Professional Classic Tech
    DARK_BG = RGBColor(15, 23, 42)      # Slate 900
    LIGHT_BG = RGBColor(248, 250, 252)  # Slate 50
    CARD_BG = RGBColor(255, 255, 255)   # White
    PRIMARY_BLUE = RGBColor(37, 99, 235) # Blue 600
    ACCENT_CYAN = RGBColor(14, 165, 233) # Sky 500
    TEXT_DARK = RGBColor(30, 41, 59)     # Slate 800
    TEXT_MUTED = RGBColor(100, 116, 139) # Slate 500
    BORDER_COLOR = RGBColor(226, 232, 240) # Slate 200
    SUCCESS_GREEN = RGBColor(22, 163, 74)

    def add_header(slide, title_text, category_text="CI/CD PIPELINE ARCHITECTURE"):
        # Category label
        tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        tf_cat = tb_cat.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = PRIMARY_BLUE
        
        # Main Title
        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.7))
        tf_title = tb_title.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_DARK

    def set_slide_background(slide, color):
        bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg_shape.fill.solid()
        bg_shape.fill.fore_color.rgb = color
        bg_shape.line.fill.background()
        return bg_shape

    def create_card(slide, left, top, width, height, title, items, badge=""):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = BORDER_COLOR
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.25)
        tf.margin_bottom = Inches(0.25)

        p0 = tf.paragraphs[0]
        if badge:
            p0.text = f"[{badge}]  {title}"
        else:
            p0.text = title
        p0.font.size = Pt(16)
        p0.font.bold = True
        p0.font.color.rgb = TEXT_DARK
        p0.space_after = Pt(10)

        for item in items:
            p = tf.add_paragraph()
            p.text = f"•  {item}"
            p.font.size = Pt(13)
            p.font.color.rgb = TEXT_MUTED
            p.space_after = Pt(6)
        return card

    # ----------------------------------------------------
    # SLIDE 1: Title Slide (Dark Classic Theme)
    # ----------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, DARK_BG)

    # Accent line top
    accent_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.2), Inches(2.5), Inches(0.08))
    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = ACCENT_CYAN
    accent_bar.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.7), Inches(3.2))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "Enterprise CI/CD Automation"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    
    p2 = tf1.add_paragraph()
    p2.text = "End-to-End Delivery Pipeline with Jenkins, Docker & Kubernetes"
    p2.font.size = Pt(22)
    p2.font.color.rgb = ACCENT_CYAN
    p2.space_before = Pt(10)

    p3 = tf1.add_paragraph()
    p3.text = "Automated Unit Testing • Multi-Stage Containerization • Docker Hub Registry • Kubernetes Orchestration & Zero-Downtime Rollouts"
    p3.font.size = Pt(14)
    p3.font.color.rgb = RGBColor(148, 163, 184)
    p3.space_before = Pt(20)

    # Info card at bottom
    info_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.2), Inches(11.7), Inches(1.4))
    info_card.fill.solid()
    info_card.fill.fore_color.rgb = RGBColor(30, 41, 59)
    info_card.line.color.rgb = RGBColor(51, 65, 85)
    tf_info = info_card.text_frame
    tf_info.margin_left = Inches(0.4)
    tf_info.margin_top = Inches(0.25)
    
    p_info = tf_info.paragraphs[0]
    p_info.text = "CORE TOOLSTACK EMPLOYED"
    p_info.font.size = Pt(11)
    p_info.font.bold = True
    p_info.font.color.rgb = PRIMARY_BLUE
    
    p_info2 = tf_info.add_paragraph()
    p_info2.text = "GitHub (SCM)  ➜  Jenkins (Automation)  ➜  Docker (Containers)  ➜  Docker Hub (Registry)  ➜  Kubernetes / kind (Cluster)"
    p_info2.font.size = Pt(15)
    p_info2.font.bold = True
    p_info2.font.color.rgb = RGBColor(241, 245, 249)
    p_info2.space_before = Pt(6)

    # ----------------------------------------------------
    # SLIDE 2: Project Overview & Objectives
    # ----------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, LIGHT_BG)
    add_header(s2, "Project Overview & Engineering Objectives", "EXECUTIVE SUMMARY")

    create_card(s2, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2), "The Problem", [
        "Manual software releases are slow, error-prone, and introduce downtime.",
        "Inconsistent environments cause the classic 'works on my machine' bug.",
        "Deployments lack automated rollback when runtime health checks fail.",
        "High barrier to reliable, multi-replica container orchestration."
    ], "CHALLENGE")

    create_card(s2, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2), "The Solution", [
        "Fully automated CI/CD pipeline triggered by every Git push.",
        "Containerized multi-stage builds guaranteeing environment parity.",
        "Centralized container image distribution via Docker Hub registry.",
        "Kubernetes orchestration with rolling updates and auto-healing."
    ], "ARCHITECTURE")

    create_card(s2, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2), "Key Outcomes", [
        "Zero-touch deployments from git commit to live cluster in ~60 seconds.",
        "Strict automated test gating preventing bad code deployment.",
        "Automated rollback triggered if smoke tests fail post-rollout.",
        "Active load balancing across healthy containerized replicas."
    ], "BENEFITS")

    # ----------------------------------------------------
    # SLIDE 3: End-to-End Pipeline Workflow
    # ----------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, LIGHT_BG)
    add_header(s3, "End-to-End CI/CD Pipeline Workflow", "PIPELINE LIFECYCLE")

    # 5 pipeline step boxes
    steps = [
        ("1. Code & Push", "Developer pushes to GitHub main branch. SCM trigger alerts Jenkins.", "GitHub"),
        ("2. Automated Test", "Docker test target runs pytest suite. Failed tests abort build.", "PyTest / Docker"),
        ("3. Package & Push", "Builds production runtime image tagged with commit SHA. Pushes to Docker Hub.", "Docker Hub"),
        ("4. K8s Rollout", "Renders image tag in manifests. Applies deployment & rolling update.", "Kubernetes"),
        ("5. Smoke & Verify", "Ephemeral curl pod verifies /health. Auto-rollback if unhealthy.", "kubectl / curl")
    ]
    box_w = Inches(2.2)
    box_h = Inches(4.8)
    for idx, (stitle, sdesc, stool) in enumerate(steps):
        left_pos = Inches(0.8 + idx * 2.4)
        c = slide_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(1.7), box_w, box_h)
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = PRIMARY_BLUE if idx in [1, 2, 3] else BORDER_COLOR
        c.line.width = Pt(1.5)
        
        tf = c.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.18)
        tf.margin_right = Inches(0.18)
        tf.margin_top = Inches(0.2)
        
        p = tf.paragraphs[0]
        p.text = stool.upper()
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = PRIMARY_BLUE
        
        p2 = tf.add_paragraph()
        p2.text = stitle
        p2.font.size = Pt(15)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_DARK
        p2.space_before = Pt(8)
        p2.space_after = Pt(12)

        p3 = tf.add_paragraph()
        p3.text = sdesc
        p3.font.size = Pt(12)
        p3.font.color.rgb = TEXT_MUTED

    # ----------------------------------------------------
    # SLIDE 4: Microservice Application Layer
    # ----------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, LIGHT_BG)
    add_header(s4, "Application Microservice Architecture (Flask)", "APPLICATION LAYER")

    create_card(s4, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "Flask Application Endpoints", [
        "Web Interface (/): Modern HTML dashboard displaying runtime pod name & version tag.",
        "Health Probe (/health): Returns JSON {'status': 'ok'} for Kubernetes liveness/readiness probes.",
        "Metadata (/version): Returns running pod hostname, build version, and system timestamp.",
        "Production WSGI: Powered by Gunicorn with 2 high-concurrency worker threads."
    ], "MICROSERVICE")

    create_card(s4, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2), "Quality Gate & Test Automation", [
        "Unit Testing Suite: Comprehensive test cases validating all application endpoints.",
        "Test Isolation: Runs inside disposable Docker container during CI build phase.",
        "Fast Execution: Test suite runs in < 0.30 seconds via pytest.",
        "Pipeline Blocker: If any test fails, image creation and deployment are immediately blocked."
    ], "TEST HARNESS")

    # ----------------------------------------------------
    # SLIDE 5: Containerization with Docker
    # ----------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, LIGHT_BG)
    add_header(s5, "Containerization Strategy: Multi-Stage Docker", "DOCKER CONTAINERIZATION")

    create_card(s5, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2), "Stage 1: Base & Test", [
        "Base on python:3.12-slim.",
        "Installs development dependencies (pytest).",
        "Executes test suite during docker build.",
        "Guarantees broken tests never leave build stage."
    ], "MULTI-STAGE")

    create_card(s5, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2), "Stage 2: Production Runtime", [
        "Zero dev-dependencies included in runtime image.",
        "Runs as non-root user (appuser UID 10001) for container security.",
        "Dynamic APP_VERSION injection via build args.",
        "Minimal attack surface and optimized layer caching."
    ], "SECURITY")

    create_card(s5, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2), "Tagging & Artifacts", [
        "Immutable tags: ${BUILD_NUMBER}-${GIT_SHORT} (e.g., 4-a60177d).",
        "Latest tag updated on every successful main release.",
        "Full traceability back to exact Git commit hash.",
        "Seamless promotion between staging and production."
    ], "TRACEABILITY")

    # ----------------------------------------------------
    # SLIDE 6: CI/CD Pipeline Automation with Jenkins
    # ----------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, LIGHT_BG)
    add_header(s6, "Pipeline Orchestration: Jenkins as Code", "JENKINS CI/CD")

    create_card(s6, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "Declarative Pipeline (Jenkinsfile)", [
        "Pipeline as Code: Pipeline definition committed directly alongside application source code.",
        "Stage Isolation: Clear boundaries for Checkout, Test, Build, Push, Deploy, and Smoke Test.",
        "Credential Masking: withCredentials binding for Docker Hub tokens and Kubernetes kubeconfig.",
        "Post-Build Cleanup: Automated cleanup of intermediate test images and Docker logout."
    ], "PIPELINE AS CODE")

    create_card(s6, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2), "Jenkins Configuration as Code (JCasC)", [
        "Zero-Touch Configuration: Jenkins plugins, credentials, and jobs defined in YAML.",
        "Automated Provisioning: Pipeline job created automatically upon container boot.",
        "Docker-in-Docker: Host Docker socket mounted for high-speed container operations.",
        "SCM Triggering: Automated repository polling and GitHub webhook readiness."
    ], "AUTOMATION")

    # ----------------------------------------------------
    # SLIDE 7: Container Registry - Docker Hub Integration
    # ----------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, LIGHT_BG)
    add_header(s7, "Registry Distribution: Docker Hub Integration", "CONTAINER REGISTRY")

    create_card(s7, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "Secure Registry Authentication", [
        "Personal Access Token (PAT): Authenticates with restricted repository permissions.",
        "Secret Management: Credentials securely stored in Jenkins credential store.",
        "Non-interactive Login: CLI authentication via secure standard input stream.",
        "Audit Trail: Push logs recorded with image digest and layer verification."
    ], "AUTHENTICATION")

    create_card(s7, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2), "Published Artifacts & Versioning", [
        "Repository: likhithkumarp07/cicd-demo.",
        "Tags Published: Version-specific tag (4-a60177d) and rolling tag (latest).",
        "Layer Reusability: Base layers cached for ultra-fast subsequent pushes.",
        "Public Accessibility: Allows Kubernetes cluster nodes to pull images reliably."
    ], "DISTRIBUTION")

    # ----------------------------------------------------
    # SLIDE 8: Kubernetes Orchestration & Deployment
    # ----------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, LIGHT_BG)
    add_header(s8, "Kubernetes Orchestration & Service Exposure", "KUBERNETES")

    create_card(s8, Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2), "Deployment Spec", [
        "Dedicated cicd-demo namespace.",
        "2 Replicas for high availability.",
        "RollingUpdate strategy (maxSurge=1, maxUnavailable=0) for zero downtime.",
        "Dynamic image tag replacement via CI sed renderer."
    ], "CONTROLLER")

    create_card(s8, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2), "Health & Reliability", [
        "Liveness Probe: Probes /health every 10s to restart hung pods.",
        "Readiness Probe: Ensures pods only receive traffic once healthy.",
        "Resource Limits: CPU (200m) and Memory (128Mi) limits to prevent starvation."
    ], "PROBES & LIMITS")

    create_card(s8, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2), "Service & Networking", [
        "Kubernetes NodePort service routing port 80 to container 5000.",
        "Kind cluster maps NodePort 30080 to host localhost:8081.",
        "Native round-robin load balancing across all active pod replicas.",
        "Verified load distribution across multiple pod IDs."
    ], "NETWORKING")

    # ----------------------------------------------------
    # SLIDE 9: Verification, Quality Gates & Rollback
    # ----------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, LIGHT_BG)
    add_header(s9, "Verification, Smoke Testing & Rollback Safety", "RESILIENCE")

    create_card(s9, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "Live Smoke Testing", [
        "In-Cluster Verification: Jenkins spawns an ephemeral curl pod inside Kubernetes.",
        "Direct Service Verification: Queries http://cicd-demo/health inside the cluster network.",
        "Immediate Pod Teardown: Ephemeral test pod cleaned up instantly upon completion.",
        "Full Pipeline Gate: Build only marked SUCCESS if cluster confirms application health."
    ], "VALIDATION")

    create_card(s9, Inches(6.9), Inches(1.6), Inches(5.6), Inches(5.2), "Automated Rollback Mechanism", [
        "Declarative post-failure action configured in Jenkinsfile.",
        "Detection: If deployment rollout hangs or smoke test returns non-200.",
        "Action: Executes kubectl rollout undo deployment/cicd-demo.",
        "Safety Guarantee: Cluster automatically reverts to last-known healthy release."
    ], "DISASTER RECOVERY")

    # ----------------------------------------------------
    # SLIDE 10: Conclusion & Production Evolution
    # ----------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, DARK_BG)

    # Accent bar top
    bar10 = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(2.5), Inches(0.08))
    bar10.fill.solid()
    bar10.fill.fore_color.rgb = ACCENT_CYAN
    bar10.line.fill.background()

    tb10 = s10.shapes.add_textbox(Inches(0.8), Inches(1.0), Inches(11.7), Inches(1.2))
    tf10 = tb10.text_frame
    p10 = tf10.paragraphs[0]
    p10.text = "Project Summary & Next Steps"
    p10.font.size = Pt(32)
    p10.font.bold = True
    p10.font.color.rgb = RGBColor(255, 255, 255)

    # 2 dark cards
    c1 = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.4), Inches(5.6), Inches(4.3))
    c1.fill.solid()
    c1.fill.fore_color.rgb = RGBColor(30, 41, 59)
    c1.line.color.rgb = RGBColor(51, 65, 85)
    tf_c1 = c1.text_frame
    tf_c1.margin_left = Inches(0.3)
    tf_c1.margin_top = Inches(0.3)
    p = tf_c1.paragraphs[0]
    p.text = "WHAT WAS ACCOMPLISHED"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    items_c1 = [
        "100% automated Git-to-Kubernetes pipeline.",
        "Containerized development, testing, and production runtime.",
        "Seamless integration with Docker Hub public registry.",
        "Zero-downtime rolling updates on a multi-replica Kubernetes cluster.",
        "Active automated health verification and rollback fail-safes."
    ]
    for item in items_c1:
        pi = tf_c1.add_paragraph()
        pi.text = f"✔  {item}"
        pi.font.size = Pt(13)
        pi.font.color.rgb = RGBColor(226, 232, 240)
        pi.space_before = Pt(8)

    c2 = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(2.4), Inches(5.6), Inches(4.3))
    c2.fill.solid()
    c2.fill.fore_color.rgb = RGBColor(30, 41, 59)
    c2.line.color.rgb = RGBColor(51, 65, 85)
    tf_c2 = c2.text_frame
    tf_c2.margin_left = Inches(0.3)
    tf_c2.margin_top = Inches(0.3)
    p = tf_c2.paragraphs[0]
    p.text = "PRODUCTION ENHANCEMENTS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    items_c2 = [
        "GitOps with ArgoCD or Flux for declarative Kubernetes state.",
        "Vulnerability scanning with Trivy / Snyk in CI build stage.",
        "Ingress controller with cert-manager for automated HTTPS/TLS.",
        "Horizontal Pod Autoscaler (HPA) driven by Prometheus metrics.",
        "Rootless container builds with Kaniko on dedicated Jenkins agents."
    ]
    for item in items_c2:
        pi = tf_c2.add_paragraph()
        pi.text = f"➔  {item}"
        pi.font.size = Pt(13)
        pi.font.color.rgb = RGBColor(226, 232, 240)
        pi.space_before = Pt(8)

    prs.save("CICD_Demo_Presentation.pptx")
    print("Presentation saved as CICD_Demo_Presentation.pptx successfully!")

if __name__ == "__main__":
    create_deck()
