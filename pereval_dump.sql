--
-- PostgreSQL database dump
--

-- Dumped from database version 15.11
-- Dumped by pg_dump version 15.11 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: coords_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.coords_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.coords_id_seq OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: coords; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.coords (
    id integer DEFAULT nextval('public.coords_id_seq'::regclass) NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    height integer NOT NULL
);


ALTER TABLE public.coords OWNER TO postgres;

--
-- Name: images_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.images_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.images_id_seq OWNER TO postgres;

--
-- Name: images; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.images (
    id integer DEFAULT nextval('public.images_id_seq'::regclass) NOT NULL,
    title text NOT NULL
);


ALTER TABLE public.images OWNER TO postgres;

--
-- Name: pereval_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pereval_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pereval_id_seq OWNER TO postgres;

--
-- Name: pereval_added; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pereval_added (
    id integer DEFAULT nextval('public.pereval_id_seq'::regclass) NOT NULL,
    date_added timestamp without time zone,
    raw_data jsonb,
    status character varying(10) DEFAULT 'new'::character varying,
    user_id integer,
    beautytitle text,
    title text,
    other_titles text,
    connect text,
    add_time timestamp without time zone,
    coord_id integer,
    winter character varying(10),
    summer character varying(10),
    autumn character varying(10),
    spring character varying(10),
    CONSTRAINT pereval_added_status_check CHECK (((status)::text = ANY ((ARRAY['new'::character varying, 'pending'::character varying, 'accepted'::character varying, 'rejected'::character varying])::text[])))
);


ALTER TABLE public.pereval_added OWNER TO postgres;

--
-- Name: pereval_added_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pereval_added_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pereval_added_id_seq OWNER TO postgres;

--
-- Name: pereval_areas_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pereval_areas_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pereval_areas_id_seq OWNER TO postgres;

--
-- Name: pereval_areas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pereval_areas (
    id bigint DEFAULT nextval('public.pereval_areas_id_seq'::regclass) NOT NULL,
    id_parent bigint NOT NULL,
    title text
);


ALTER TABLE public.pereval_areas OWNER TO postgres;

--
-- Name: pereval_images; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pereval_images (
    pereval_id integer NOT NULL,
    image_id integer NOT NULL
);


ALTER TABLE public.pereval_images OWNER TO postgres;

--
-- Name: pereval_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pereval_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pereval_user_id_seq OWNER TO postgres;

--
-- Name: untitled_table_200_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.untitled_table_200_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.untitled_table_200_id_seq OWNER TO postgres;

--
-- Name: spr_activities_types; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.spr_activities_types (
    id integer DEFAULT nextval('public.untitled_table_200_id_seq'::regclass) NOT NULL,
    title text
);


ALTER TABLE public.spr_activities_types OWNER TO postgres;

--
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    fam character varying NOT NULL,
    name character varying NOT NULL,
    otc character varying,
    phone character varying(12) NOT NULL,
    email character varying NOT NULL
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer DEFAULT nextval('public.pereval_user_id_seq'::regclass) NOT NULL,
    fam text NOT NULL,
    name text NOT NULL,
    otc text NOT NULL,
    phone character varying(15) NOT NULL,
    email text NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Data for Name: coords; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.coords (id, latitude, longitude, height) VALUES
(42, 43.355, 42.439, 5642),
(43, 47.8901, 91.2345, 3120),
(44, -45.678, 60.123, 3200),
(45, 27.9881, 86.925, 7906),
(46, 37.7749, -80.4194, 1200),
(47, 65.123, -20.456, 1500);


--
-- Data for Name: images; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.images (id, title) VALUES
(1, 'Седловина'),
(2, 'Подъем');


--
-- Data for Name: pereval_added; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.pereval_added (
    id, date_added, raw_data, status, user_id, beautytitle, title, other_titles, connect, add_time, coord_id, winter, summer, autumn, spring
) VALUES
    (41, NULL, NULL, 'new', 12, 'Перевал Казад-Дум', 'Морийский перевал', 'Врата Мории; Перевал Друэдайн', 'Связи нет', '2024-01-15 08:30:45.123', 44, '2A', '2A', '2A', '2A'),
    (43, NULL, NULL, 'accepted', 13, 'Перевал Нью-Ривер', 'Нью-Ривер', 'Аппалачский перевал, Голубой хребет', 'Хорошая связь', '2023-11-22 14:20:10.456', 46, '2А', '1Б', '1Б', '2А'),
    (42, NULL, NULL, 'new', 2, 'Южное седло Эвереста', 'Перевал Эверест', 'Сагарматха; Джомолунгма', 'Нет связи', '2024-03-05 09:45:30.789', 45, '3А', '2Б', '2А', '2Б'),
    (39, NULL, NULL, 'new', 1, 'Гора Эльбрус', 'Эльбрус', 'Минги-Тау; Гора двух вершин', 'Отличная связь', '2023-12-31 23:59:59.999', 42, '3Б', '2А', '2Б', '3А'),
    (44, NULL, NULL, 'pending', 14, 'Перевал Ледяного Ветра', 'Ледяной перевал', 'Врата Севера, Дорога за Стену', 'Слабая связь', '2024-02-14 12:00:00', 47, '3Б', '2Б', '2А', '3А');


--
-- Data for Name: pereval_areas; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.pereval_areas (id, id_parent, title) VALUES
(0, 0, 'Планета Земля'),
(1, 0, 'Памиро-Алай'),
(65, 0, 'Алтай'),
(66, 65, 'Северо-Чуйский хребет'),
(88, 65, 'Южно-Чуйский хребет'),
(92, 65, 'Катунский хребет'),
(105, 1, 'Фанские горы'),
(106, 1, 'Гиссарский хребет (участок западнее перевала Анзоб)'),
(131, 1, 'Матчинский горный узел'),
(133, 1, 'Горный узел Такали, Туркестанский хребет'),
(137, 1, 'Высокий Алай'),
(147, 1, 'Кичик-Алай и Восточный Алай'),
(367, 375, 'Аладаглар'),
(375, 0, 'Тавр'),
(384, 0, 'Саяны'),
(386, 65, 'Хребет Листвяга'),
(387, 65, 'Ивановский хребет'),
(388, 65, 'Массив Мунгун-Тайга'),
(389, 65, 'Хребет Цаган-Шибэту'),
(390, 65, 'Хребет Чихачева (Сайлюгем)'),
(391, 65, 'Шапшальский хребет'),
(392, 65, 'Хребет Южный Алтай'),
(393, 65, 'Хребет Монгольский Алтай'),
(398, 384, 'Западный Саян'),
(399, 384, 'Восточный Саян'),
(402, 384, 'Кузнецкий Алатау'),
(459, 65, 'Курайский хребет');

--
-- Data for Name: pereval_images; Type: TABLE DATA; Schema: public; Owner: postgres
--

--INSERT INTO public.pereval_images (pereval_id, image_id) VALUES


--
-- Data for Name: spr_activities_types; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.spr_activities_types (id, title) VALUES
(1, 'пешком'),
(2, 'лыжи'),
(3, 'катамаран'),
(4, 'байдарка'),
(5, 'плот'),
(6, 'сплав'),
(7, 'велосипед'),
(8, 'автомобиль'),
(9, 'мотоцикл'),
(10, 'парус'),
(11, 'верхом');


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

--INSERT INTO public."user" (id, fam, name, otc, phone, email) VALUES



--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.users (id, fam, name, otc, phone, email) VALUES
(1, 'Пупкин', 'Василий', 'Иванович', '79031234567', 'user@email.tld'),
(2, 'Скайуокер', 'Люк', 'Энакинович', '+9777777', 'maytheForcebewithU@email.gal'),
(3, 'Иванов', 'Иван', 'Иванович', '89991234567', 'ivanov@example.com'),
(4, 'Сидоров', 'Петр', 'Иванович', '9999999999', 'sidorov@example.com'),
(7, 'Петров', 'Петр', 'Петрович', '9999999990', 'petrov@example.com'),
(9, 'Старк', 'Эддард', 'Рикардович', '79123456789', 'eddard.stark@winterfell.com'),
(11, 'Тестовый', 'Тестим', 'Тестович', '12345678912', 'testim@gmail.com'),
(12, 'Торбинс', 'Фродо', 'Бэггинс', '89997776655', 'frodo@shire.com'),
(13, 'Смит', 'Джон', 'Майкл', '89998887766', 'smith@appalachian.com'),
(14, 'Сноу', 'Джон', 'Эддардович', '89997776655', 'jon.snow@nightwatch.com');


--
-- Name: coords_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.coords_id_seq', 47, true);


--
-- Name: images_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.images_id_seq', 2, true);


--
-- Name: pereval_added_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pereval_added_id_seq', 1, false);


--
-- Name: pereval_areas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pereval_areas_id_seq', 1, false);


--
-- Name: pereval_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pereval_id_seq', 44, true);


--
-- Name: pereval_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pereval_user_id_seq', 14, true);


--
-- Name: untitled_table_200_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.untitled_table_200_id_seq', 1, false);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_id_seq', 1, false);


--
-- Name: coords coords_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.coords
    ADD CONSTRAINT coords_pkey PRIMARY KEY (id);


--
-- Name: images images_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_pkey PRIMARY KEY (id);


--
-- Name: pereval_added pereval_added_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pereval_added
    ADD CONSTRAINT pereval_added_pkey PRIMARY KEY (id);


--
-- Name: pereval_areas pereval_areas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pereval_areas
    ADD CONSTRAINT pereval_areas_pkey PRIMARY KEY (id);


--
-- Name: pereval_images pereval_images_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pereval_images
    ADD CONSTRAINT pereval_images_pkey PRIMARY KEY (pereval_id, image_id);


--
-- Name: spr_activities_types spr_activities_types_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.spr_activities_types
    ADD CONSTRAINT spr_activities_types_pkey PRIMARY KEY (id);


--
-- Name: user user_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_email_key UNIQUE (email);


--
-- Name: user user_phone_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_phone_key UNIQUE (phone);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_user_id ON public."user" USING btree (id);


--
-- Name: pereval_added fk_coords; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pereval_added
    ADD CONSTRAINT fk_coords FOREIGN KEY (coord_id) REFERENCES public.coords(id);


--
-- Name: pereval_added fk_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pereval_added
    ADD CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: pereval_images pereval_images_image_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pereval_images
    ADD CONSTRAINT pereval_images_image_id_fkey FOREIGN KEY (image_id) REFERENCES public.images(id) ON DELETE CASCADE;


--
-- Name: pereval_images pereval_images_pereval_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pereval_images
    ADD CONSTRAINT pereval_images_pereval_id_fkey FOREIGN KEY (pereval_id) REFERENCES public.pereval_added(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

