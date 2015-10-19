\c openfire;


CREATE TABLE asim_enterprise_device
(
  id serial NOT NULL,
  device_serial_no character varying(60) NOT NULL,
  device_type character varying(60) NOT NULL,
  interface_type character varying(20) DEFAULT NULL::character varying,
  username character varying(128) DEFAULT NULL::character varying,
  bindtime integer NOT NULL DEFAULT 0,
  publishtime integer NOT NULL DEFAULT 0,
  CONSTRAINT asim_enterprise_device_pkey PRIMARY KEY (id),
  CONSTRAINT asim_enterprise_device_device_serial_no_key UNIQUE (device_serial_no)
);

CREATE TABLE asim_import_akey_task
(
  id serial NOT NULL,
  task_name character varying(60) NOT NULL,
  file_name character varying(60) NOT NULL,
  task_status character varying(20) NOT NULL,
  
  upload_time integer NOT NULL DEFAULT 0,
  start_time integer NOT NULL DEFAULT 0,
  finish_time integer NOT NULL DEFAULT 0,
  
  total_item integer DEFAULT 0,
  finish_item integer DEFAULT 0,
  failed_item integer DEFAULT 0,
  
  CONSTRAINT asim_import_akey_task_pkey PRIMARY KEY (id),
  CONSTRAINT asim_import_akey_task_task_name_key UNIQUE (task_name)
);


CREATE TABLE asim_import_task_process_info
(
  id serial NOT NULL,
  import_task_id serial NOT NULL,
  task_name character varying(60) NOT NULL,
  file_name character varying(60) NOT NULL,
  
  upload_time integer NOT NULL DEFAULT 0,
  finish_time integer DEFAULT 0,
  
  total_item integer DEFAULT 0,
  failed_item integer DEFAULT 0,
  
  failed_info character varying(1024) NOT NULL,
  
  CONSTRAINT asim_import_task_process_info_pkey PRIMARY KEY (id),
  CONSTRAINT asim_import_task_process_info_task_name_key UNIQUE (task_name)
);

CREATE TABLE asim_user_log_collection
(
  id serial NOT NULL,
  username character varying(60) NOT NULL,
  logurl character varying(1024),
  status character varying(60),
  start_time character varying(60) NOT NULL ,
  end_time character varying(60) NOT NULL ,
  finish_time character varying(60) ,
  
  CONSTRAINT asim_user_log_collection_pkey PRIMARY KEY (id)
);

