CREATE OR REPLACE VIEW public.thunder_view AS
 SELECT thunder.id,
    thunder."Idfu",
    thunder."Geb.Datum",
    thunder."Date.Intake",
    thunder."Institute",
    thunder."Gender",
    thunder."cT",
    thunder."cN",
    thunder."Date.of.birth",
    thunder."Age",
    thunder."FF",
    thunder."LF",
    thunder."TotalDose",
    thunder."OK",
    thunder."Ok.type",
    thunder."pT.stage",
    thunder."pN.stage",
    thunder."TRG..1.4.",
    thunder."Date.OK",
    thunder."WHO",
    date_part('year'::text, thunder."Date.Intake")::integer AS year_intake,
    date_part('month'::text, thunder."Date.Intake")::integer AS month_intake,
    date_part('day'::text, thunder."Date.Intake")::integer AS day_intake,
    (date_part('year'::text, thunder."FF") - date_part('year'::text, thunder."Date.of.birth"))::integer AS age_at_start_rt,
    (date_part('year'::text, thunder."Date.Intake") - date_part('year'::text, thunder."Date.of.birth"))::integer AS age_at_diagnosis,
        CASE
            WHEN thunder."Institute" = 1 THEN 'http://www.maastro.nl'::text
            WHEN thunder."Institute" = 2 THEN 'http://www.gemelli-art.it'::text
            ELSE NULL::text
        END AS institute_url,
        CASE
            WHEN thunder."Gender" = false THEN 'ncit:C16576'::text
            WHEN thunder."Gender" = true THEN 'ncit:C20197'::text
            ELSE NULL::text
        END AS gender_class,
        CASE
            WHEN thunder."WHO" = 0 THEN 'ncit:C105722'::text
            WHEN thunder."WHO" = 1 THEN 'ncit:C105723'::text
            WHEN thunder."WHO" = 2 THEN 'ncit:C105725'::text
            WHEN thunder."WHO" = 3 THEN 'ncit:C105726'::text
            WHEN thunder."WHO" = 4 THEN 'ncit:C105727'::text
            WHEN thunder."WHO" = 5 THEN 'ncit:C105728'::text
            ELSE NULL::text
        END AS who_class,
        CASE
            WHEN thunder."cT" = 1 THEN 'ncit:C48720'::text
            WHEN thunder."cT" = 2 THEN 'ncit:C48724'::text
            WHEN thunder."cT" = 3 THEN 'ncit:C48728'::text
            WHEN thunder."cT" = '-1'::integer THEN 'ncit:C48732'::text
            ELSE NULL::text
        END AS ct_class,
        CASE
            WHEN thunder."cN" = 0 THEN 'ncit:C48705'::text
            WHEN thunder."cN" = 1 THEN 'ncit:C48706'::text
            WHEN thunder."cN" = 2 THEN 'ncit:C48786'::text
            WHEN thunder."cN" = 3 THEN 'ncit:C48714'::text
            WHEN thunder."cN" = '-1'::integer THEN 'ncit:C48718'::text
            ELSE NULL::text
        END AS cn_class,
        CASE
            WHEN thunder."pT.stage" = 1 THEN 'ncit:C48720'::text
            WHEN thunder."pT.stage" = 2 THEN 'ncit:C48724'::text
            WHEN thunder."pT.stage" = 3 THEN 'ncit:C48728'::text
            WHEN thunder."pT.stage" = 4 THEN 'ncit:C48732'::text
            ELSE NULL::text
        END AS pt_class,
        CASE
            WHEN thunder."pN.stage" = 0 THEN 'ncit:C48705'::text
            WHEN thunder."pN.stage" = 1 THEN 'ncit:C48706'::text
            WHEN thunder."pN.stage" = 2 THEN 'ncit:C48786'::text
            WHEN thunder."pN.stage" = 3 THEN 'ncit:C48714'::text
            WHEN thunder."pN.stage" = '-1'::integer THEN 'ncit:C48718'::text
            ELSE NULL::text
        END AS pn_class
   FROM thunder;