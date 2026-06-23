<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Painel Assinador</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <header>
        <div class="container">
            <h1>Painel do Assinador</h1>
            <nav>
                <span>Olá, {{ current_user.username }}</span>
                <a href="{{ url_for('logout') }}" class="btn-logout">Sair</a>
            </nav>
        </div>
    </header>

    <main class="container">
        <section class="docs-section">
            <h2>Documentos Pendentes de Assinatura</h2>
            {% if docs %}
            <table>
                <thead>
                    <tr>
                        <th>Arquivo</th>
                        <th>Fluxo</th>
                        <th>Ação</th>
                    </tr>
                </thead>
                <tbody>
                    {% for doc in docs %}
                    <tr>
                        <td>{{ doc.original_filename }}</td>
                        <td>Fluxo {{ doc.workflow_type }}</td>
                        <td>
                            <form action="{{ url_for('sign', doc_id=doc.id) }}" method="POST" enctype="multipart/form-data" class="sign-form">
                                <input type="file" name="signature" accept="image/*" required id="sig-{{ doc.id }}" style="display:none" onchange="this.form.submit()">
                                <button type="button" class="btn-primary btn-sm" onclick="document.getElementById('sig-{{ doc.id }}').click()">Assinar Agora</button>
                            </form>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <p>Nenhum documento pendente no momento.</p>
            {% endif %}
        </section>

        <section class="history-section">
            <h2>Meu Histórico</h2>
            <table>
                <thead>
                    <tr>
                        <th>Arquivo</th>
                        <th>Ação Realizada</th>
                        <th>Data/Hora</th>
                    </tr>
                </thead>
                <tbody>
                    {% for log in history %}
                    <tr>
                        <td>{{ log.document.original_filename }}</td>
                        <td>{{ log.action }}</td>
                        <td>{{ log.timestamp.strftime('%d/%m/%Y %H:%M') }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </section>
    </main>
</body>
</html>
