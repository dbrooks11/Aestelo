import logging
import os
import requests
from typing import Any, Dict

import structlog
from flask import Flask, g, request, json
from structlog.processors import JSONRenderer, TimeStamper
from structlog.stdlib import ProcessorFormatter

def add_request_id(logger: Any, method_name: str, event_dict: Dict) -> Dict:
    """Add request ID to all log entries for traceability"""
    if hasattr(g, 'request_id'):
        event_dict['request_id'] = g.request_id
    return event_dict

def add_user_id(logger: Any, method_name: str, event_dict: Dict) -> Dict:
    """Add current user ID to logs when available"""
    if hasattr(g, 'current_user_id'):
        event_dict['user_id'] = g.current_user_id
    return event_dict

def add_ip_address(logger: Any, method_name: str, event_dict: Dict) -> Dict:
    """Add client IP address for security auditing"""
    if request:
        forwarded = request.headers.get('X-Forwarded-For')
        if forwarded:
            event_dict['ip'] = forwarded.split(',')[0].strip()
        elif request.remote_addr:
            event_dict['ip'] = request.remote_addr
    return event_dict

def configure_logging(app: Flask) -> None:
    """Configure structured logging for production"""
    
    log_level = logging.DEBUG if app.debug else logging.INFO

    if app.debug:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        )
        logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    else:
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,        
                structlog.stdlib.add_logger_name,           
                structlog.stdlib.add_log_level,           
                structlog.stdlib.PositionalArgumentsFormatter(),  
                add_request_id,                             
                add_user_id,                               
                add_ip_address,                            
                TimeStamper(fmt="iso"),                   
                structlog.processors.StackInfoRenderer(),  
                structlog.processors.format_exc_info,       
                JSONRenderer(indent=None)                   
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
        
        log_format = "%(message)s"
        logging.basicConfig(
            format=log_format,
            level=log_level,
            handlers=[logging.StreamHandler()]
        )
        
        handler = logging.StreamHandler()
        handler.setFormatter(ProcessorFormatter())
        
        app.logger.handlers.clear()
        app.logger.addHandler(handler)
        app.logger.setLevel(log_level)
        
        
        logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
        
        app.logger.info("Logging configured", 
                    environment=os.getenv('FLASK_ENV', 'development'),
                    log_level=log_level)

def get_logger(name: str):
    """Get a structlog logger instance for a module"""
    return structlog.get_logger(name)



class BetterStackHandler(logging.Handler):
    def emit(self, record):
        try:
            requests.post(
                "https://in.logs.betterstack.com/",
                headers={"Authorization": "Bearer YOUR_TOKEN"},
                json={"logs": [json.loads(record.getMessage())]}
            )
        except:
            pass  