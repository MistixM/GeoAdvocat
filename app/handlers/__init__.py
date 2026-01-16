from .start import start_router
from .launch import launch_router
from .help import help_router
from .change_topic_prompt import change_topic
from .change_comment_prompt import change_comment
from .change_queries import change_queries_router
from .show import show_router


routers = [start_router,
           launch_router, 
           help_router,
           change_topic,
           change_comment,
           change_queries_router,
           show_router]