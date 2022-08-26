
-- COMMAND TO INSTALL A MYSQL SERVER ON DOCKER
-- > docker run --name mysql -p 3306:3306 -v mysql_volume:/var/lib/mysql/ -d -e "MYSQL_ROOT_PASSWORD=password" mysql


CREATE DATABASE IF NOT EXISTS iot_project_db;

USE iot_project_db;

CREATE TABLE IF NOT EXISTS configuration (
    land_id int(11) NOT NULL,
    node_id int(11) NOT NULL,
    status boolean NOT NULL DEFAULT true,
    last_timestamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    irr_enabled boolean NOT NULL,
    irr_limit int(11) NOT NULL,
    irr_duration int(11) NOT NULL,
    mst_timer int(11) NOT NULL,
    ph_timer int(11) NOT NULL,
    light_timer int(11) NOT NULL,
    tmp_timer int(11) NOT NULL,
    PRIMARY KEY (land_id, node_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS land (
    land_id int(11) NOT NULL AUTO_INCREMENT,
    area float NOT NULL,
    locality varchar(100) NOT NULL,
    crop varchar(100) NOT NULL,
    soil_type varchar(100) NOT NULL,
    mst_trashold int(11) NOT NULL,
    min_ph int(11) NOT NULL,
    max_ph int(11) NOT NULL,
    min_light int(11) NOT NULL,
    max_light int(11) NOT NULL,
    min_tmp int(11) NOT NULL,
    max_tmp int(11) NOT NULL,
    PRIMARY KEY(land_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS measurement (
    land_id int(11) NOT NULL,
    node_id int(11) NOT NULL,
    m_timestamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    sensor varchar(100) NOT NULL,
    m_value int(11) NOT NULL,
    PRIMARY KEY(land_id, node_id, m_timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS violation (
    land_id int(11) NOT NULL,
    node_id int(11) NOT NULL,
    v_timestamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    sensor varchar(100) NOT NULL,
    v_value int(11) NOT NULL,
    PRIMARY KEY(land_id, node_id, v_timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS irrigation (
    land_id int(11) NOT NULL,
    node_id int(11) NOT NULL,
    i_timestamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    irr_status boolean NOT NULL,
    PRIMARY KEY(land_id, node_id, i_timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;






