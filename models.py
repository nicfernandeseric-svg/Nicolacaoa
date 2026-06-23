<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Painel Administrador</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <header>
        <div class="container">
            <h1>Painel Administrador</h1>
            <nav>
                <span>Olá, {{ current_user.username }}</span>
                <a href="{{ url_for('logout') }}" class="btn-logout">Sair</a>
            </nav>
        </div>
    </header>

    <main class="container">
        <section class="stats-grid">
            <div class="stat-card">
                <h3>Total</h3>
                <p>{{ stats.total }}</p>
            </div>
            <div class="stat-card">
                <h3>Pendentes</h3>
                <p>{{ stats.pending }}</p>
            </div>
            <div class="stat-card">
                <h3>Em Assinatura</h3>
                <p>{{ stats.in_progress }}</p>
            </div>
            <div class="stat-card">
                <h3>Concluídos</h3>
                <p>{{ stats.completed }}</p>
            </div>
        </section>

        <section class="upload-section">
            <h2>Enviar Novos Documentos</h2>
            <form action="{{ url_for('upload') }}" method="POST" enctype="multipart/form-data">
                <div class="form-row">
                    <div class="form-group">
                        <label>Selecione os PDFs:</label>
                        <input type="file" name="pdfs" multiple accept=".pdf" required>
                    </div>
                    <div class="form-group">
                        <label>Escolha o Fluxo:</label>
                        <select name="workflow" required>
                            <option value="A">Fluxo A (Admin → Assinador 1)</option>
                            <option value="B">Fluxo B (Admin → Assinador 2 → Assinador 1)</option>
                        </select>
                    </div>
                    <button type="submit" class="btn-primary">Enviar e Iniciar Fluxo</button>
                </div>
            </form>
        </section>

        <section class="docs-section">
            <h2>Gestão de Documentos</h2>
            <form action="{{ url_for('download_batch') }}" method="POST">
                <div class="table-actions">
                    <button type="submit" name="download_selected" class="btn-secondary">Baixar Selecionados</button>
                    <button type="submit" name="download_all" class="btn-secondary">Baixar Todos (.ZIP)</button>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th><input type="checkbox" id="select-all"></th>
                            <th>Arquivo</th>
                            <th>Data Upload</th>
                            <th>Fluxo</th>
                            <th>Status</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for doc in docs %}
                        <tr>
                            <td>
                                {% if doc.status == 'COMPLETED' %}
                                <input type="checkbox" name="doc_ids" value="{{ doc.id }}">
                                {% endif %}
                            </td>
                            <td>{{ doc.original_filename }}</td>
                            <td>{{ doc.upload_date.strftime('%d/%m/%Y %H:%M') }}</td>
                            <td>Fluxo {{ doc.workflow_type }}</td>
                            <td><span class="badge badge-{{ doc.status.lower() }}">{{ doc.status }}</span></td>
                            <td>
                                <a href="{{ url_for('download_single', doc_id=doc.id) }}" class="btn-sm">Baixar</a>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </form>
        </section>
    </main>

    <script>
        document.getElementById('select-all').onclick = function() {
            var checkboxes = document.getElementsByName('doc_ids');
            for (var checkbox of checkboxes) {
                checkbox.checked = this.checked;
            }
        }
    </script>
</body>
</html>
