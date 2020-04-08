DROP TABLE IF EXISTS Usuario;
DROP TABLE IF EXISTS Video;
DROP TABLE IF EXISTS Lista;
DROP TABLE IF EXISTS ListaVideo;
DROP TABLE IF EXISTS UsuarioLista;
DROP TABLE IF EXISTS Transmision;

CREATE TABLE Usuario(
	id					INTEGER PRIMARY KEY AUTOINCREMENT,
	user				VARCHAR NOT NULL,
	ipUsuario			VARCHAR NOT NULL,
	password			VARCHAR NOT NULL
);

CREATE TABLE Video(
	id					INTEGER PRIMARY KEY AUTOINCREMENT,
	nombre				VARCHAR NOT NULL,
	puerto				VARCHAR NOT NULL,
	ruta				VARCHAR,
	FOREIGN KEY(id) REFERENCES Usuario(id)
);

CREATE TABLE Lista(
	id 					INTEGER PRIMARY KEY AUTOINCREMENT,
	nombre				VARCHAR NOT NULL
);

CREATE TABLE ListaVideo(
	id_lista			INT,
	id_video			INT,
	FOREIGN KEY(id_lista) REFERENCES Lista(id),
	FOREIGN KEY(id_video) REFERENCES Video(id),
	PRIMARY KEY (id_lista, id_video)
);

CREATE TABLE UsuarioLista(
	id_usuario			INT,
	id_lista			INT,
	FOREIGN KEY(id_usuario) REFERENCES Usuario(id),
	FOREIGN KEY(id_lista) REFERENCES Lista(id),
	PRIMARY KEY (id_usuario, id_lista)
);

CREATE TABLE Transmision(
	id_video 			INT NOT NULL,
	id_usuario			INT NOT NULL,
	puerto				INT NOT NULL,
	ip_usuario			VARCHAR NOT NULL
);

INSERT INTO Usuario values (null,"rommy","192.168.0.7","pass");
INSERT INTO Video values (null,"Arbolito","25565","../videos/video.mp4");
INSERT INTO Video values (null,"Lapiz","25565","../videos/prueba2.mp4");
-- INSERT INTO Video values (null,"otro video","25565",null);
-- INSERT INTO Lista values (null,"lista de prueba");
-- INSERT INTO ListaVideo values (1,1);
-- INSERT INTO ListaVideo values (1,2);
-- INSERT INTO UsuarioLista values (1,1);
-- INSERT INTO Transmision values (1,1,25565,"127.0.0.1");