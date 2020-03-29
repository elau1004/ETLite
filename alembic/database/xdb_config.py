xdb_map = {
    'db2' : {
        # TODO: Fill this out.
    }
    ,'sqlite' : {
        # SQLite requires an INT data type for auto increment.
        # SEE: https://www.sqlite.org/datatype3.html
         'autoinc'      :'AUTOINCREMENT'
        ,'bit0'         :'BOOLEAN         NOT NULL  DEFAULT 0 '
        ,'bit1'         :'BOOLEAN         NOT NULL  DEFAULT 1 '
        ,'bin16'        :'BLOB'
        ,'chr01'        :'CHAR(1)'
        ,'clstr0'       :''
        ,'clstr1'       :''
        ,'comment'      :'-- '
        ,'int08'        :'INTEGER'  # Enum lookup shouldn't have many entries.
        ,'int16'        :'INTEGER'
        ,'int32'        :'INTEGER'
        ,'int64'        :'INTEGER'
        ,'json'         :'JSON'
        ,'len'          :'LENGTH'
        ,'idtt'         :''
        ,'real'         :'FLOAT'
        ,'txt08'        :'VARCHAR(8)'
        ,'txt16'        :'VARCHAR(16)'
        ,'txt32'        :'VARCHAR(32)'
        ,'txt64'        :'VARCHAR(64)'
        ,'txt128'       :'VARCHAR(128)'
        ,'txtmax'       :'TEXT'
        ,'utcdtm'       :'DATETIME'
        ,'utcdft'       :'CURRENT_TIMESTAMP'
        ,'utcupd'       :'DATETIME        NOT NULL  DEFAULT CURRENT_TIMESTAMP'
    }
    ,'mssql' : {
         'autoinc'      :'IDENTITY(100,1)'
        ,'bit0'         :'BIT             NOT NULL  DEFAULT 0 '
        ,'bit1'         :'BIT             NOT NULL  DEFAULT 1 '
        ,'bin16'        :'BINARY(16)'
        ,'chr01'        :'CHAR(1)'
        ,'clstr0'       :'NONCLUSTERED '
        ,'clstr1'       :'CLUSTERED    '
        ,'comment'      :'-- '
        ,'len'          :'LEN'
        ,'idtt'         :'IDENTITY(100,1)'
        ,'int08'        :'TINYINT'   # Enum lookup shouldn't have many entries.
        ,'int16'        :'SMALLINT'
        ,'int32'        :'INTEGER'
        ,'int64'        :'BIGINT'
        ,'json'         :'NVARCHAR(MAX)'
        ,'real'         :'FLOAT'
        ,'txt08'        :'NVARCHAR(8)'
        ,'txt16'        :'NVARCHAR(16)'
        ,'txt32'        :'NVARCHAR(32)'
        ,'txt64'        :'NVARCHAR(64)'
        ,'txt128'       :'NVARCHAR(128)'
        ,'txtmax'       :'NVARCHAR(MAX)'
        ,'utcdtm'       :'DATETIMEOFFSET'
        ,'utcdft'       :'SYSDATETIMEOFFSET()'
        ,'utcupd'       :'DATETIMEOFFSET  NOT NULL  DEFAULT SYSDATETIMEOFFSET()'
    }
    ,'mysql' : {
        # TODO: Fill this out.
    }
    ,'oracle' : {       # https://docs.oracle.com/cd/B19306_01/gateways.102/b14270/apa.htm
         'autoinc'      :''
        ,'bit0'         :'NUMBER(1,0)     NOT NULL  DEFAULT 0 '
        ,'bit1'         :'NUMBER(1,0)     NOT NULL  DEFAULT 1 '
        ,'bin16'        :'RAW(16)'
        ,'chr01'        :'CHAR(1)'
        ,'clstr0'       :'NONCLUSTERED '
        ,'clstr1'       :'CLUSTERED    '
        ,'comment'      :'-- '
        ,'len'          :'LENGTH'
        ,'idtt'         :'GENERATED BY DEFAULT AS   IDENTITY  START WITH 100'
        ,'int08'        :'NUMBER(3)'    # Enum lookup shouldn't have many entries.
        ,'int16'        :'NUMBER(5)'
        ,'int32'        :'NUMEBER(10)'
        ,'int64'        :'NUMEBER(19)'
        ,'json'         :'NCLOB'
        ,'real'         :'FLOAT'
        ,'txt08'        :'NVARCHAR2(8)'
        ,'txt16'        :'NVARCHAR2(16)'
        ,'txt32'        :'NVARCHAR2(32)'
        ,'txt64'        :'NVARCHAR2(64)'
        ,'txt128'       :'NVARCHAR2(128)'
        ,'txtmax'       :'NCLOB'
        ,'utcdtm'       :'TIMESTAMP WITH TIME ZONE'
        ,'utcdft'       :'CURRENT_TIMESTAMP'
        ,'utcupd'       :'TIMESTAMP WITH TIME ZONE  NOT NULL DEFAULT CURRENT_TIMESTAMP'
    }
    ,'postgresql' : {
        # TODO: Fill this out.
    }
}
