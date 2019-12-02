Use mydb;


CREATE Table articles (id int primary key, name text,	affiliation text,	citedby	int, pub_title	text, pub_year	int, pub_url text,	journal text);
LOAD DATA INFILE "C:/MySQL Server 8.0/Uploads/articles.csv" IGNORE INTO TABLE articles  
FIELDS TERMINATED BY ","  ENCLOSED BY '"' LINES TERMINATED BY "\r\n" 
IGNORE 1 lines;

CREATE Table journal_list ( journal text, journal_id int not null primary key, field text);
LOAD DATA INFILE "C:/MySQL Server 8.0/Uploads/journalslist.csv" INTO TABLE journal_list 
FIELDS TERMINATED BY "," OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY "\n" 
IGNORE 1 lines;

CREATE Table university (country_region varchar(30), field varchar(30),	institution varchar(100), link text, subject text,
	total_score varchar(30), total_score_award varchar(30), total_score_cnci varchar(30), total_score_ic varchar(30), total_score_pub varchar(30), total_score_top varchar(30),
	world_rank varchar(20));
    
LOAD DATA INFILE "C:/MySQL Server 8.0/Uploads/university_ranking.csv" INTO TABLE university ;
