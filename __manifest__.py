{
    'name': 'Project Agile Extension',
    'version': '1.0',
    'summary': 'Extensión del módulo de Proyectos para Metodologías Ágiles',
    'description': """
        Añade funcionalidades y campos adicionales al módulo de Proyectos para seguir metodologías ágiles.
    """,
    'depends': ['project', 'hr'],
    'data': [
        'views/project_views.xml',
       
    ],
    'installable': True,
    'application': False,
}
