-- postgresql은 테이블 생성 시 enum 바로 사용 못함. 
-- 테이블 생성 전, type을 enum으로 정해줌.
CREATE TYPE status AS ENUM ('active','deleted','blocked');
CREATE TYPE sns_type AS ENUM ('FB', 'G', 'K', 'Email');


-- table 생성
create table users(
  id  SERIAL primary key,
  status status default 'active' not null,
  email           varchar(255) null,
  pw              varchar(2000) null,
  name            varchar(255) null,
  phone_number    varchar(20) null,
  profile_img     varchar(1000) null,
  sns_type        sns_type null,
  marketing_agree boolean default false null,
  updated_at      timestamp default 'now'::timestamp not null,
  created_at      timestamp default 'now'::timestamp not null
);

-- postgresql은 onupdate이 없어 함수를 만들고 트리거를 걸어주어야
-- update 시의 시간을 timestamp로 찍어줄 수 있음.
-- 함수 'update_updated_at_column' 생성
CREATE FUNCTION update_updated_at_column() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
  BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
  END;
$$;
 
-- 트리거 users_updated_at_modtime 생성
CREATE TRIGGER users_updated_at_modtime BEFORE UPDATE ON users FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

insert into users(name) values('코알라');
update users set name='hello' where id=1;

create table users(
  id  SERIAL primary key,
  status status default 'active' not null,
  email           varchar(255) null,
  pw              varchar(2000) null,
  name            varchar(255) null,
  phone_number    varchar(20) null,
  profile_img     varchar(1000) null,
  sns_type        sns_type null,
  marketing_agree boolean default false null,
  updated_at      timestamp without time zone not null,
  created_at      timestamp without time zone not null
);
