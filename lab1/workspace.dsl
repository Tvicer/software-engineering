workspace {
    name "Atlassian Jira"
    !identifiers hierarchical

    model {
        user = person "Пользователь" {
            description "Пользователь системы Atlassian Jira"
        }

        jiraSystem = softwareSystem "Система Atlassian Jira" {
            description "Система управления проектами и задачами"

            apiService = container "API Service" {
                technology "Java / Spring Boot"
                description "Backend-сервис, реализующий бизнес-логику"
            }

            database = container "Database" {
                technology "PostgreSQL"
                description "Основная база данных системы"
            }

            user -> apiService "Использует систему через API" "REST/JSON"
            apiService -> database "SQL-запросы" "POSTGRESQL"
        }
    }

    views {
        themes default

        systemContext jiraSystem {
            include *
            autolayout lr
        }

        container jiraSystem {
            include *
            autolayout lr
        }

        dynamic jiraSystem "create_user" "Создание нового пользователя" {
            autoLayout lr
            user -> jiraSystem.apiService "POST /api/v1/user/create"
            jiraSystem.apiService -> jiraSystem.database "Сохраняет данные пользователя"
        }

        dynamic jiraSystem "search_user_by_login" "Поиск пользователя по логину" {
            autoLayout lr
            user -> jiraSystem.apiService "GET /api/v1/user/search/login"
            jiraSystem.apiService -> jiraSystem.database "Получает данные пользователя"
        }

        dynamic jiraSystem "search_user_by_name" "Поиск пользователя по имени и фамилии" {
            autoLayout lr
            user -> jiraSystem.apiService "POST /api/v1/user/search"
            jiraSystem.apiService -> jiraSystem.database "Получает данные пользователя"
        }

        dynamic jiraSystem "create_project" "Создание проекта" {
            autoLayout lr
            user -> jiraSystem.apiService "POST /api/v1/project/create"
            jiraSystem.apiService -> jiraSystem.database "Сохраняет данные проекта"
        }

        dynamic jiraSystem "search_project_by_name" "Поиск проекта по имени" {
            autoLayout lr
            user -> jiraSystem.apiService "GET /api/v1/project/search"
            jiraSystem.apiService -> jiraSystem.database "Получает данные проекта"
        }

        dynamic jiraSystem "get_all_projects" "Получение всех проектов" {
            autoLayout lr
            user -> jiraSystem.apiService "GET /api/v1/projects"
            jiraSystem.apiService -> jiraSystem.database "Получает список проектов"
        }

        dynamic jiraSystem "create_task" "Создание задачи в проекте" {
            autoLayout lr
            user -> jiraSystem.apiService "POST /api/v1/task/create"
            jiraSystem.apiService -> jiraSystem.database "Сохраняет данные задачи"
        }

        dynamic jiraSystem "get_all_tasks_in_project" "Получение всех задач в проекте" {
            autoLayout lr
            user -> jiraSystem.apiService "GET /api/v1/tasks"
            jiraSystem.apiService -> jiraSystem.database "Получает список задач"
        }

        dynamic jiraSystem "get_task_by_code" "Получение задачи по коду" {
            autoLayout lr
            user -> jiraSystem.apiService "GET /api/v1/task"
            jiraSystem.apiService -> jiraSystem.database "Получает данные задачи"
        }
    }
}