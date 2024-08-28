from odoo import models, fields, api

# Modelo de Historias de Usuario
class ProjectUserStory(models.Model):
    _name = 'project.user.story'
    _description = 'Historias de Usuario del Proyecto'

    name = fields.Char(string="Título de la Historia de Usuario", required=True)
    project_id = fields.Many2one('project.project', string="Proyecto", required=True, ondelete='cascade')
    description = fields.Text(string="Descripción", help="Descripción de la historia de usuario en formato Markdown.")
    tasks_ids = fields.One2many('project.task', 'user_story_id', string="Tareas Relacionadas")
    markdown_content = fields.Html(string="Contenido en Markdown")

    @api.model
    def create(self, vals):
        # Aquí puedes añadir cualquier lógica adicional necesaria al crear una historia de usuario
        return super(ProjectUserStory, self).create(vals)

class ProjectTask(models.Model):
    _inherit = 'project.task'

    # Relación Many2one con las Historias de Usuario
    user_story_id = fields.Many2one('project.user.story', string="Historia de Usuario", ondelete='set null')


# Modelo para Hitos del Proyecto
class ProjectMilestone(models.Model):
    _name = 'project.milestone'
    _description = 'Hitos del Proyecto'

    name = fields.Char(string="Nombre del Hito", required=True)
    project_id = fields.Many2one('project.project', string="Proyecto", ondelete='cascade')
    start_date = fields.Date(string="Fecha de Inicio")
    end_date = fields.Date(string="Fecha de Finalización")
    tasks_ids = fields.One2many('project.task', 'milestone_id', string="Tareas Relacionadas")
    progress = fields.Float(string="Progreso (%)")
    is_reached = fields.Boolean(string="Hito Alcanzado", default=False)
    deadline = fields.Date(string="Fecha Límite") 

# Modelo para Dependencias de Proyectos
class ProjectDependency(models.Model):
    _name = 'project.dependency'
    _description = 'Dependencias del Proyecto'

    project_id = fields.Many2one('project.project', string="Proyecto Principal", required=True, ondelete='cascade')
    dependent_project_id = fields.Many2one('project.project', string="Proyecto Dependiente", required=True)
    description = fields.Text(string="Descripción de la Dependencia")
    status = fields.Selection([('not_started', 'No Iniciado'), ('in_progress', 'En Progreso'), ('done', 'Completado')], string="Estado", default='not_started')

# Modelo para Métricas de Calidad
class ProjectQualityMetric(models.Model):
    _name = 'project.quality.metric'
    _description = 'Métricas de Calidad del Proyecto'

    name = fields.Char(string="Nombre de la Métrica", required=True)
    project_id = fields.Many2one('project.project', string="Proyecto", ondelete='cascade')
    objective = fields.Text(string="Objetivo de la Métrica")
    result = fields.Text(string="Resultado de la Métrica")

# Modelo para la Mitigación de Riesgos
class ProjectRiskMitigation(models.Model):
    _name = 'project.risk.mitigation'
    _description = 'Plan de Mitigación de Riesgos del Proyecto'

    project_id = fields.Many2one('project.project', string="Proyecto", required=True, ondelete='cascade')
    name = fields.Char(string="Título del Plan de Mitigación", required=True)
    steps = fields.Text(string="Pasos de Mitigación")
    responsible_user_id = fields.Many2one('res.users', string="Responsable")
    deadline = fields.Date(string="Fecha Límite")

# Extensión del Modelo de Proyecto
class ProjectProject(models.Model):
    _inherit = 'project.project'

    # Campos Nuevos y Extendidos
    milestone_ids = fields.One2many('project.milestone', 'project_id', string="Hitos")
    risk_description = fields.Text(string="Descripción de Riesgos")
    mitigation_plan_ids = fields.One2many('project.risk.mitigation', 'project_id', string="Planes de Mitigación de Riesgos")
    dependencies_ids = fields.One2many('project.dependency', 'project_id', string="Dependencias del Proyecto")
    client_satisfaction_score = fields.Float(string="Puntuación de Satisfacción del Cliente")
    quality_metrics_ids = fields.One2many('project.quality.metric', 'project_id', string="Métricas de Calidad")
    sprint_goal = fields.Text(string="Objetivo del Sprint")
    total_defects = fields.Integer(string="Total de Defectos")
    user_story_ids = fields.One2many('project.user.story', 'project_id', string="Historias de Usuario")
    planned_deadline = fields.Date(string="Fecha Planificada")  # Agregar este campo

    # Campos Calculados
    risk_score = fields.Float(string="Puntuación de Riesgo", compute='_compute_risk_score')
    quality_index = fields.Float(string="Índice de Calidad", compute='_compute_quality_index')
    dependency_status = fields.Selection([('no_dependencies', 'Sin Dependencias'), ('incomplete', 'Dependencias Incompletas'), ('complete', 'Dependencias Completas')], string="Estado de Dependencias", compute='_compute_dependency_status')
    earned_value = fields.Float(string="Valor Ganado", compute='_compute_earned_value')
    schedule_variance = fields.Float(string="Varianza de Programación", compute='_compute_schedule_variance')
    cost_variance = fields.Float(string="Varianza de Costo", compute='_compute_cost_variance')

    # Otros Campos del Proyecto
    budget = fields.Monetary(string="Presupuesto", currency_field='currency_id')
    actual_hours = fields.Float(string="Horas Reales Trabajadas", compute='_compute_actual_hours')
    velocity = fields.Float(string="Velocidad del Equipo", compute='_compute_velocity')
    progress_percentage = fields.Float(string="Porcentaje de Progreso", compute='_compute_progress_percentage')
    burn_rate = fields.Float(string="Burn Rate", compute='_compute_burn_rate')
    completion_forecast = fields.Date(string="Pronóstico de Finalización", compute='_compute_completion_forecast')
    story_points = fields.Integer(string="Puntos de Historia")
    sprint_length = fields.Integer(string="Duración del Sprint (días)")
    repository_url = fields.Char(string="URL del Repositorio")
    documentation_url = fields.Char(string="URL de Documentación")
    risk_level = fields.Selection([('low', 'Bajo'), ('medium', 'Medio'), ('high', 'Alto')], string="Nivel de Riesgo")
    assigned_team_id = fields.Many2one('hr.department', string="Equipo Asignado")

    # Métodos Calculados
    @api.depends('risk_description', 'mitigation_plan_ids')
    def _compute_risk_score(self):
        for project in self:
            # Ejemplo simple de lógica para calcular la puntuación de riesgo basada en la descripción y el plan de mitigación
            project.risk_score = len(project.risk_description) * (1 if project.mitigation_plan_ids else 2)

    @api.depends('quality_metrics_ids', 'total_defects', 'client_satisfaction_score')
    def _compute_quality_index(self):
        for project in self:
            # Índice de calidad basado en las métricas de calidad, defectos y satisfacción del cliente
            if project.total_defects and project.client_satisfaction_score:
                project.quality_index = (sum(metric.result for metric in project.quality_metrics_ids) - project.total_defects) * project.client_satisfaction_score / 100
            else:
                project.quality_index = 0

    @api.depends('dependencies_ids')
    def _compute_dependency_status(self):
        for project in self:
            if not project.dependencies_ids:
                project.dependency_status = 'no_dependencies'
            elif all(dep.status == 'done' for dep in project.dependencies_ids):
                project.dependency_status = 'complete'
            else:
                project.dependency_status = 'incomplete'

    @api.depends('progress_percentage', 'budget', 'actual_hours')
    def _compute_earned_value(self):
        for project in self:
            # Valor ganado basado en el progreso y presupuesto del proyecto
            project.earned_value = (project.progress_percentage / 100) * project.budget if project.budget else 0

    @api.depends('progress_percentage', 'planned_deadline', 'completion_forecast')
    def _compute_schedule_variance(self):
        for project in self:
            # Varianza de programación basada en el progreso y fechas planificadas vs. estimadas
            if project.planned_deadline and project.completion_forecast:
                project.schedule_variance = (fields.Date.from_string(project.planned_deadline) - fields.Date.from_string(project.completion_forecast)).days
            else:
                project.schedule_variance = 0

    @api.depends('burn_rate', 'budget', 'actual_hours')
    def _compute_cost_variance(self):
        for project in self:
            # Varianza de costos basada en el presupuesto consumido vs. el presupuesto total
            budget_spent = project.actual_hours * project.env['hr.employee'].search([]).hourly_rate
            project.cost_variance = budget_spent - project.budget if project.budget else 0
