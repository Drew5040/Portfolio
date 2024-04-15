from flask import render_template
from log_config import logger


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        logger.debug("Exception 400: bad request...")
        return render_template('error_handlers/400.html'), 400

    @app.errorhandler(401)
    def unauthorized(error):
        logger.debug("Exception 401: unauthorized...")
        return render_template('error_handlers/401.html'), 401

    @app.errorhandler(403)
    def forbidden(error):
        logger.debug("Exception 403: forbidden...")
        return render_template('error_handlers/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        logger.debug("Exception 404: page not found...")
        return render_template('error_handlers/404.html'), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        logger.debug("Exception 405: method not allowed...")
        return render_template('error_handlers/405.html'), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        logger.debug('Exception 500: internal server error...')
        return render_template('error_handlers/500.html'), 500

    @app.errorhandler(502)
    def bad_gateway(error):
        logger.debug("Exception 502: bad_gateway...")
        return render_template('error_handlers/502.html'), 502

    @app.errorhandler(503)
    def service_unavailable(error):
        logger.debug("Exception 503: service unavailable...")
        return render_template('error_handlers/503.html'), 503

    @app.errorhandler(504)
    def gateway_timeout(error):
        logger.debug("Exception 504: gateway_timeout")
        return render_template('error_handlers/504.html'), 504

    @app.errorhandler(Exception)
    def handle_exception(error):
        # Handle generic exception
        logger.debug("Uncaught exception occurred. Check logs...")
        return render_template('error.html'), 500
