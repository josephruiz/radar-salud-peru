-- Radar Salud Perú 2026–2031. Run manually in a NEW Supabase project.
create extension if not exists pgcrypto;
create extension if not exists pg_trgm;
create table if not exists public.sources(
 id uuid primary key default gen_random_uuid(),
 name text not null unique,
 homepage text not null,
 source_type text not null check(source_type in ('official','news','research','aggregator')),
 enabled boolean not null default true,
 created_at timestamptz not null default now()
);
create table if not exists public.records(
 id uuid primary key default gen_random_uuid(),
 source_id uuid references public.sources(id),
 canonical_url text not null unique,
 title text not null,
 summary text,
 category text not null check(category in ('noticia','norma','alerta','indicador')),
 published_at timestamptz,
 discovered_at timestamptz not null default now(),
 territory_name text,
 ubigeo text,
 geographic_confidence text not null default 'unverified' check(geographic_confidence in ('unverified','title_match','source_verified')),
 review_status text not null default 'unreviewed' check(review_status in ('unreviewed','verified','rejected')),
 source_kind text not null default 'aggregator',
 metadata jsonb not null default '{}'::jsonb,
 search_text tsvector generated always as (to_tsvector('spanish', coalesce(title,'')||' '||coalesce(summary,''))) stored,
 constraint records_ubigeo_format check (ubigeo is null or ubigeo ~ '^[0-9]{6}$')
);
create index if not exists records_search_idx on public.records using gin(search_text);
create index if not exists records_date_idx on public.records(published_at desc);
create index if not exists records_territory_idx on public.records(territory_name);
create table if not exists public.legal_changes(
 id uuid primary key default gen_random_uuid(),
 record_id uuid not null references public.records(id),
 changed_record_id uuid references public.records(id),
 relationship text not null check(relationship in ('amends','repeals','regulates','cites','unknown')),
 article_ref text, evidence text, potential_impact text,
 verified boolean not null default false,
 created_at timestamptz not null default now()
);
create table if not exists public.indicators(
 id uuid primary key default gen_random_uuid(),
 source_id uuid references public.sources(id),
 code text not null, name text not null, territory_ubigeo text,
 period_start date not null, period_end date not null,
 value numeric not null, unit text not null,
 methodology text, denominator numeric, source_url text not null,
 created_at timestamptz not null default now(),
 unique(code,territory_ubigeo,period_start,period_end,source_url)
);
create table if not exists public.collection_runs(
 id uuid primary key default gen_random_uuid(),
 source_id uuid references public.sources(id),
 started_at timestamptz not null default now(),
 ended_at timestamptz, status text not null default 'running'
 check(status in ('running','success','partial','failed')),
 discovered_count integer not null default 0,
 error_log jsonb not null default '[]'::jsonb
);
-- No anonymous writes or raw publication access by default.
alter table public.sources enable row level security;
alter table public.records enable row level security;
alter table public.legal_changes enable row level security;
alter table public.indicators enable row level security;
alter table public.collection_runs enable row level security;
insert into public.sources(name,homepage,source_type) values
('Diario Oficial El Peruano','https://diariooficial.elperuano.pe/Normas','official'),
('Google News RSS','https://news.google.com/','aggregator')
on conflict(name) do nothing;
