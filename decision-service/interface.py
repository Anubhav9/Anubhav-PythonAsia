import config
import logging
import constants


def get_current_deployment_platform():
    """
    Helper function to get the current deployment platform. Infrastructure details is being fetched basis this.
    :return: Name of the deployment platform. Current options include AWS,GCP & Alibaba Cloud. Otherwise Invalid returned
    """
    current_deployment_platform = config.deployment_platform.upper()
    allowed_deployment_platforms = [constants.DEPLOYMENT_PLATFORM_AWS,constants.DEPLOYMENT_PLATFORM_GCP]
    if current_deployment_platform not in allowed_deployment_platforms:
        logging.error(f"[Deployment Platform]: Invalid Deployment Platform is set.")
        return "INVALID"
    return current_deployment_platform


def create_and_get_infra_details_map():
    """
    Helper function which creates the infra map which has details / urls of the infra components.
    :return: Map containing the url of the infra components depending upon the current deployment platform
    """
    current_deployment_platform = get_current_deployment_platform()
    logging.info(f"[Deployment Platform]: Current Deployment Platform set is: {current_deployment_platform}")

    ## All Nomenclature follow DEPLOYMENT_PLATFORM+INFRA. Add everything in the below section
    value_database_host_key = f"{current_deployment_platform}_DATABASE_HOST"
    value_database_host = getattr(config,value_database_host_key)


    ## All Infra Details needs to be updated here so that we have a single source
    infra_details_map = {}
    infra_details_map["deployment_platform"]=current_deployment_platform
    infra_details_map["database_host"]=value_database_host

    logging.debug(f"[INFRA_DETAILS_MAP]: The current infra details map is: {infra_details_map}")
    return infra_details_map
