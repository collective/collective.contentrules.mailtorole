from zope.i18nmessageid import MessageFactory
import logging


mailtoroleMessageFactory = MessageFactory(
    'collective.contentrules.mailtorole')
logger = logging.getLogger(__name__)


def initialize(context):
    """Intializer called when used as a Zope 2 product."""
