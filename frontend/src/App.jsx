const modules = [
  {
    title: 'Acadêmico',
    description: 'Gestão de alunos, turmas, matrículas, frequência, avaliações, histórico e boletins.'
  },
  {
    title: 'Pedagógico',
    description: 'Planejamento de aulas, conteúdos por turma, registros pedagógicos e relatórios individuais.'
  },
  {
    title: 'Financeiro',
    description: 'Mensalidades, pagamentos, inadimplência, bolsas e relatórios exportáveis.'
  },
  {
    title: 'Administrativo',
    description: 'Professores, funcionários, perfis, permissões e auditoria centralizada.'
  },
  {
    title: 'Relatórios & Dashboard',
    description: 'Indicadores acadêmicos, financeiros e gráficos com filtros por período.'
  }
];

const highlights = [
  { label: 'Local-first', value: 'On-premise com Docker + PocketBase' },
  { label: 'Segurança', value: 'LGPD, consentimentos, logs e exportação de dados' },
  { label: 'Escalabilidade', value: 'Arquitetura modular e pronta para multiescola' }
];

const quickAccess = [
  'Cadastro de alunos',
  'Matrículas e turmas',
  'Fluxo financeiro',
  'Relatórios instantâneos',
  'Configurações de branding'
];

export default function App() {
  return (
    <div className="app">
      <header className="hero">
        <div>
          <p className="eyebrow">Anjos EduTech ERP</p>
          <h1>É Tempo de Crescer – Centro Educacional</h1>
          <p className="subtitle">
            Plataforma completa para gestão escolar, com foco em simplicidade operacional e evolução contínua.
          </p>
          <div className="cta-group">
            <button className="primary">Acessar Painel</button>
            <button className="ghost">Guia de Configuração</button>
          </div>
        </div>
        <div className="hero-card">
          <h3>Visão Geral</h3>
          <ul>
            {highlights.map((item) => (
              <li key={item.label}>
                <strong>{item.label}</strong>
                <span>{item.value}</span>
              </li>
            ))}
          </ul>
        </div>
      </header>

      <section className="modules">
        <div className="section-title">
          <h2>Módulos do ERP</h2>
          <p>Estrutura modular com integrações futuras e API documentada.</p>
        </div>
        <div className="grid">
          {modules.map((module) => (
            <article key={module.title} className="card">
              <h3>{module.title}</h3>
              <p>{module.description}</p>
              <button className="link">Ver detalhes</button>
            </article>
          ))}
        </div>
      </section>

      <section className="config">
        <div>
          <h2>Branding configurável</h2>
          <p>
            Defina cores institucionais, logo da escola e rodapé com razão social para padronizar toda a
            comunicação.
          </p>
          <div className="tags">
            <span>Logo personalizável</span>
            <span>Cores institucionais</span>
            <span>Rodapé institucional</span>
            <span>Interface responsiva</span>
          </div>
        </div>
        <div className="config-card">
          <h4>Acesso rápido</h4>
          <ol>
            {quickAccess.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ol>
        </div>
      </section>

      <section className="status">
        <div>
          <h2>Pronto para operações locais</h2>
          <p>
            Hospedagem local com backups automáticos do PocketBase e controle de acesso por perfil.
          </p>
        </div>
        <div className="pill-group">
          <span>Docker Compose</span>
          <span>Volumes persistentes</span>
          <span>Auditoria e logs</span>
          <span>Exportação LGPD</span>
        </div>
      </section>

      <footer className="footer">
        <div>
          <strong>É Tempo de Crescer – Centro Educacional</strong>
          <p>Razão social: Centro Educacional É Tempo de Crescer LTDA.</p>
        </div>
        <div>
          <p>Suporte local • API integrada • Ambiente seguro</p>
        </div>
      </footer>
    </div>
  );
}
