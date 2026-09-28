"""Sentinel's interface expressed as FastHTML components.

Local CSS and JavaScript preserve the supplied design and browser interactions.
The browser calls /ask and /health on this same FastHTML application.
"""
import json
from .catalog import security_policy, static_catalog
from fasthtml.common import (
    A, Aside, B, Body, Br, Button, Dialog, Div, Footer, Form, H1,
    Head, Header, Html, I, Input, Kbd, Label, Link, Main, Meta, Nav,
    Noscript, P, Script, Section, Small, Span, Strong, Textarea, Title,
)
from starlette.staticfiles import StaticFiles
from .config import ROOT

ASSETS = ROOT.parent / 'static' / 'sentinel'


def icon(name, **kwargs):
    return Span(data_icon=name, **kwargs)


def action(name, *children, **kwargs):
    return Button(*children, type='button', data_action=name, **kwargs)


def sidebar():
    return Aside(
        A(Span('✦', cls='brand-mark'), Span('sentinel', Span('.', cls='brand-dot')),
          Span('AI', cls='version'), cls='brand', href='/', aria_label='Sentinel home'),
        action('new', icon('plus'), ' New conversation ', Kbd('Ctrl K'), cls='new-chat'),
        Div('WORKSPACE', cls='nav-label'),
        Nav(
            action('chat', icon('chat'), 'AI assistant', Span('✦', cls='nav-badge'), cls='nav-item active'),
            action('library', icon('grid'), 'Prompt library', Span('12', cls='nav-count', id='prompt-count'), cls='nav-item'),
            action('data', icon('database'), 'Data explorer', cls='nav-item'), cls='workspace-nav'),
        Div(Span('YOUR CONVERSATIONS', cls='nav-label'),
            action('search', icon('search'), cls='icon-button', aria_label='Search conversations'), cls='history-heading'),
        Label(icon('search'), Input(id='history-search', placeholder='Search chats…', aria_label='Search conversations'), cls='history-search'),
        Div(id='history', cls='history'),
        Div(
            Div(icon('shield', cls='workspace-emblem'),
                Div(Strong('Your data. Your answers.'), P('Grounded in your operations.')),
                Span('✦', cls='tiny-star'), cls='workspace-card'),
            action('settings', icon('settings'), 'Settings & connection', cls='nav-item'),
            Div(Span('YO', cls='avatar'), Div(Strong('Your workspace'), Small('Local session')),
                action('help', icon('help'), cls='icon-button', aria_label='Help'), cls='profile'), cls='sidebar-bottom'),
        cls='sidebar', id='sidebar', aria_label='Main navigation')


def topbar():
    return Header(
        Div(action('menu', icon('menu'), cls='icon-button mobile-menu', aria_label='Open navigation'),
            Span('Workspace', cls='breadcrumb-root'), Span('/', cls='slash'),
            Span('AI assistant', id='page-label'), cls='breadcrumbs'),
        Div(action('settings', Span(cls='status-dot'), Span('Checking API', id='health-label'),
                   id='health-pill', cls='health-pill'),
            Span(cls='top-separator'),
            action('theme', icon('sun'), cls='icon-button', aria_label='Toggle light or dark theme'),
            Span('YO', cls='avatar small'), cls='top-actions'), cls='topbar')


def prompt_card(index, name, title, description):
    return Button(
        Div(Span(icon(name), cls='card-icon'), Span('↗', cls='arrow'), cls='card-top'),
        Strong(title), P(description), cls='prompt-card', data_prompt=str(index), type='button')


def welcome():
    return Div(
        Div(Div(Span('✦', cls='mini-orbit'), ' INTELLIGENCE, AT YOUR SERVICE', cls='eyebrow'),
            Div(Span('✦'), I(), B('✧'), cls='hero-symbol', aria_hidden='true'),
            H1('Your operations.', Br(), Span('A conversation away.')),
            P('Turn questions into clarity. Explore your security data', Br(cls='desktop-break'),
              ' with an assistant that understands your business.'), cls='intro'),
        Section(Div(Span('A little inspiration to get started'), icon('arrow-down'), cls='section-heading'),
            Div(prompt_card(0, 'shield', 'Get the bigger picture', 'A quick look at your guard workforce.'),
                prompt_card(1, 'pin', 'Explore your sites', 'Know the places behind your operations.'),
                prompt_card(2, 'briefcase', 'Know your customers', 'Get to know your customer base.'),
                id='prompt-cards', cls='prompt-grid'), cls='suggestions', aria_label='Suggested questions'),
        Div(icon('shield'), ' Read-only insights ', Span('·'), ' Grounded answers ', Span('·'),
            ' Your data stays with your backend', cls='scope-note'), id='welcome', cls='welcome')


def conversation():
    return Section(
        Div(Div(Span('CONVERSATION', cls='eyebrow'), H1('New conversation', id='conversation-title')),
            action('export-chat', icon('download'), 'Export', cls='text-button'), cls='conversation-heading'),
        Div(id='messages', aria_live='polite', aria_relevant='additions'),
        Div(Span('✦', cls='assistant-avatar'),
            Div(Strong('Preparing your request', Span('…', cls='thinking-dots'), id='thinking-title'),
                P('Connecting to the assistant.', id='thinking-detail')), Span('0s', id='elapsed'),
            id='thinking', cls='thinking', hidden=True),
        Div(id='chat-bottom'), id='conversation', cls='conversation', hidden=True)


def composer(question=''):
    return Footer(
        Div(Form(Label('Ask about your operations', fr='question', cls='sr-only'),
            Textarea(question, id='question', rows=2, maxlength=4000,
                     placeholder='Ask about shifts, attendance, incidents, guards, or other operations…'),
            Div(Span(Span('✦', cls='mini-orbit'), ' Operations assistant ', Span(cls='model-divider'),
                Span(icon('lock'), 'Read only', cls='read-only'), cls='model-chip'),
                Div(Span('0 / 4,000', id='char-count'),
                    action('stop', 'Stop waiting', id='stop-button', cls='text-button', hidden=True),
                    Button(icon('arrow-up'), id='send-button', type='submit', cls='send-button',
                           aria_label='Send question', disabled=True), cls='send-controls'), cls='composer-bottom'),
            id='ask-form'), cls='composer-shell'),
        Div(Span('Answers backed by data. Review the SQL and results for context.'),
            Span('Enter to send ', Span('↵', cls='key-symbol')), cls='composer-caption'),
        id='composer-area', cls='composer-area')


def sentinel_page(question=''):
    policy = security_policy()
    configured = static_catalog()['tables']
    domains = [{'table': table, 'description': configured.get(table, {}).get('description', table.replace('_', ' '))}
               for table in policy['allowed_tables'] if table not in policy.get('blocked_tables', [])]
    return Html(
        Head(Meta(charset='UTF-8'), Meta(name='viewport', content='width=device-width,initial-scale=1'),
            Meta(name='theme-color', content='#111014'), Title('Sentinel — Your operations, in conversation'),
            Link(rel='icon', href='/static/sentinel/favicon.svg'),
            Link(rel='stylesheet', href='/static/sentinel/styles.css'),
            Script(src='/static/sentinel/app.js', type='module')),
        Body(A('Skip to conversation', href='#main', cls='skip'),
            Div(sidebar(), action('close-menu', cls='sidebar-scrim', aria_label='Close navigation'),
                Div(topbar(), Main(welcome(), conversation(),
                    Section(id='library', cls='content-view', hidden=True),
                    Section(id='data-view', cls='content-view', hidden=True, data_domains=json.dumps(domains)), id='main', tabindex='-1'),
                    composer(question[:4000]), cls='main-shell'), cls='app-shell'),
            Dialog(Div(id='modal-content'), id='modal'), Div(id='toast', role='status', hidden=True),
            Noscript('Enable JavaScript to use Sentinel chat, prompt library, and conversation history.')),
        lang='en', data_theme='dark')


def register_ui(app):
    app.mount('/static/sentinel', StaticFiles(directory=str(ASSETS)), name='sentinel-static')

    @app.route('/', methods=['GET'])
    def home():
        return sentinel_page()

    @app.route('/chat', methods=['GET'])
    def chat_page(question: str = ''):
        return sentinel_page(question)
