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

COPY public.coords (id, latitude, longitude, height) FROM stdin;
1	45.3842	7.1525	1200
2	42.1234	74.5678	3000
3	61.7542	59.1269	1079
4	45.6789	120.5432	3100
\.


--
-- Data for Name: images; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.images (id, title) FROM stdin;
1	Седловина
2	Подъем
\.


--
-- Data for Name: pereval_added; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pereval_added (id, date_added, raw_data, status, user_id, beautytitle, title, other_titles, connect, add_time, coord_id, winter, summer, autumn, spring) FROM stdin;
3	\N	\N	new	\N	Мглистые горы	Тестовая запись	Еще одна запись	Связь	2025-02-20 00:00:00	2	\N	\N	\N	\N
4	\N	\N	new	\N	перевал Дятлова	Дятлов	Dyatlov Pass; Перевал Холатчхаль	Связь отсутствует	2025-02-21 12:00:00	3	3Б			
5	\N	\N	accepted	2	Перевал Драконьего Клыка	Перевал Драконьего Клыка	Драконий Путь; Клык Дракона	Соединяет земли эльфов с королевством драконов	2025-02-21 12:00:00	4	A1	B2	C1	A2
1	2022-02-21 14:14:00.720184	{"beautyTitle": "пер. "}	new	1	пер. 	Пхия	Триев		2021-09-22 13:18:13	1		1А	1А	
\.


--
-- Data for Name: pereval_areas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pereval_areas (id, id_parent, title) FROM stdin;
0	0	Планета Земля
1	0	Памиро-Алай
65	0	Алтай
66	65	Северо-Чуйский хребет
88	65	Южно-Чуйский хребет
92	65	Катунский хребет
105	1	Фанские горы
106	1	Гиссарский хребет (участок западнее перевала Анзоб)
131	1	Матчинский горный узел
133	1	Горный узел Такали, Туркестанский хребет
137	1	Высокий Алай
147	1	Кичик-Алай и Восточный Алай
367	375	Аладаглар
375	0	Тавр
384	0	Саяны
386	65	Хребет Листвяга
387	65	Ивановский хребет
388	65	Массив Мунгун-Тайга
389	65	Хребет Цаган-Шибэту
390	65	Хребет Чихачева (Сайлюгем)
391	65	Шапшальский хребет
392	65	Хребет Южный Алтай
393	65	Хребет Монгольский Алтай
398	384	Западный Саян
399	384	Восточный Саян
402	384	Кузнецкий Алатау
459	65	Курайский хребет
\.


--
-- Data for Name: pereval_images; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pereval_images (pereval_id, image_id) FROM stdin;
\.


--
-- Data for Name: spr_activities_types; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.spr_activities_types (id, title) FROM stdin;
1	пешком
2	лыжи
3	катамаран
4	байдарка
5	плот
6	сплав
7	велосипед
8	автомобиль
9	мотоцикл
10	парус
11	верхом
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (id, fam, name, otc, phone, email) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, fam, name, otc, phone, email) FROM stdin;
1	Пупкин	Василий	Иванович	79031234567	user@email.tld
2	Скайуокер	Люк	Энакинович	+9777777	maytheForcebewithU@email.gal
\.


--
-- Name: coords_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.coords_id_seq', 4, true);


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

SELECT pg_catalog.setval('public.pereval_id_seq', 5, true);


--
-- Name: pereval_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pereval_user_id_seq', 2, true);


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

