
-- COMMAND TO INSTALL A MYSQL SERVER ON DOCKER
-- > docker run --name mysql -p 3306:3306 -v mysql_volume:/var/lib/mysql/ -d -e "MYSQL_ROOT_PASSWORD=password" mysql
-- INSTALL MYSQL CONNECTOP
-- > python3 -m pip install mysql-connector-python

DROP DATABASE IF EXISTS iot_project_db;
CREATE DATABASE IF NOT EXISTS iot_project_db;

USE iot_project_db;

CREATE TABLE IF NOT EXISTS configuration (
    land_id int(11) NOT NULL,
    node_id int(11) NOT NULL,
    protocol varchar(100) DEFAULT NULL,
    status varchar(100) NOT NULL DEFAULT "online",
    last_timestamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    irr_enabled varchar(100) NOT NULL,
    irr_limit int(11) NOT NULL,
    irr_duration int(11) NOT NULL,
    mst_timer int(11) NOT NULL,
    ph_timer int(11) NOT NULL,
    light_timer int(11) NOT NULL,
    tmp_timer int(11) NOT NULL,
    PRIMARY KEY (land_id, node_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO configuration (land_id, node_id, protocol, status, last_timestamp, irr_enabled, irr_limit, irr_duration, mst_timer, ph_timer, light_timer, tmp_timer) VALUES
(1, 0, 'null', 'online', CURRENT_TIMESTAMP, 'null', 22, 20, 720, 720, 30, 60),
(2, 0, 'null', 'online', CURRENT_TIMESTAMP, 'null', 25, 25, 720, 1440, 60, 120),
(3, 0, 'null', 'online', CURRENT_TIMESTAMP, 'null', 20, 20, 1440, 1440, 120, 120),
(4, 0, 'null', 'online', CURRENT_TIMESTAMP, 'null', 20, 15, 1440, 720, 60, 60),
(5, 0, 'null', 'online', CURRENT_TIMESTAMP, 'null', 15, 20, 720, 2880, 60, 120);

CREATE TABLE IF NOT EXISTS land (
    id int(11) NOT NULL,
    area float NOT NULL,
    locality varchar(100) NOT NULL,
    name varchar(100) NOT NULL, 
    crop varchar(100) NOT NULL,
    soil_type varchar(100) NOT NULL,
    mst_trashold int(11) NOT NULL,
    min_ph int(11) NOT NULL,
    max_ph int(11) NOT NULL,
    min_tmp int(11) NOT NULL,
    max_tmp int(11) NOT NULL,
    PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO land (id, area, locality, name, crop, soil_type, mst_trashold, min_ph, max_ph, min_tmp, max_tmp) VALUES
(1, 0.1, 'pag 5, part 4, Carbognano (VT)', 'Fondi', 'lettuce', 'loam', 14, 6, 7, 4, 22),
(2, 0.5, 'pag 2 part 1 Carbognano (VT)', 'Crafeno', 'tomato', 'silt loam', 11, 6, 7, 10, 25),
(3, 1, 'pag 4 part 5 Carbognano (VT)', 'Filaro', 'olive', 'clay loam', 22, 5, 7, 16, 33),
(4, 2, 'pag 3 part 2 Carbognano (VT)', 'Galli', 'olive', 'sandy loam', 8, 6, 8, 18, 36),
(5, 1, 'pag 8 part 3 Carbognano (VT)', 'Corpiè', 'apple', 'slity clay', 27, 6, 8, 20, 38); 

CREATE TABLE IF NOT EXISTS measurement (
    land_id int(11) NOT NULL,
    node_id int(11) NOT NULL,
    m_timestamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    sensor varchar(100) NOT NULL,
    m_value int(11) NOT NULL,
    PRIMARY KEY(land_id, node_id, m_timestamp, sensor)
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
    irr_status varchar(100) NOT NULL,
    PRIMARY KEY(land_id, node_id, i_timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;






