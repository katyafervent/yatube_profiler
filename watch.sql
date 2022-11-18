-- No related
SELECT
       "posts_post"."id", "posts_post"."text", "posts_post"."pub_date", "posts_post"."author_id",
       "posts_post"."group_id", "posts_post"."image"
FROM "posts_post"
ORDER BY "posts_post"."pub_date" DESC

-- select_related
SELECT
       "posts_post"."id", "posts_post"."text", "posts_post"."pub_date", "posts_post"."author_id",
       "posts_post"."group_id", "posts_post"."image",
       "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_superuser",
       "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email",
       "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."date_joined",
       "posts_group"."id", "posts_group"."title", "posts_group"."slug", "posts_group"."description"
FROM "posts_post"
     INNER JOIN "auth_user" ON ("posts_post"."author_id" = "auth_user"."id")
     LEFT OUTER JOIN "posts_group" ON ("posts_post"."group_id" = "posts_group"."id")
ORDER BY "posts_post"."pub_date" DESC

-- prefetch_related
SELECT
       "posts_post"."id", "posts_post"."text", "posts_post"."pub_date", "posts_post"."author_id",
       "posts_post"."group_id", "posts_post"."image"
FROM "posts_post"
ORDER BY "posts_post"."pub_date" DESC

-- inner select
SELECT
       "posts_post"."id", "posts_post"."text", "posts_post"."pub_date", "posts_post"."author_id",
       "posts_post"."group_id", "posts_post"."image", "auth_user"."id", "auth_user"."password",
       "auth_user"."last_login", "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name",
       "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff", "auth_user"."is_active",
       "auth_user"."date_joined"
FROM "posts_post" INNER JOIN "auth_user" ON ("posts_post"."author_id" = "auth_user"."id")
ORDER BY "posts_post"."pub_date" DESC, "posts_post"."id" DESC LIMIT 1000


SELECT
       "posts_group"."id", "posts_group"."title", "posts_group"."slug", "posts_group"."description"
FROM "posts_group"
WHERE "posts_group"."id" IN (70251, 70252, 70253, 70254, 70255, 70256, 70257, 70258, 70259, 70260, 70261, 70262, 70263, 70264, 70265, 70266, 70267, 70268, 70269, 70270, 70271, 70272, 70273, 70274, 70275, 70276, 70277, 70278, 70279, 70280, 70281, 70282, 70283, 70284, 70285, 70286, 70287, 70288, 70289, 70290, 70291, 70292, 70293, 70294, 70295, 70296, 70297, 70298, 70299, 70300, 70301, 70302, 70303, 70304, 70305, 70306, 70307, 70308, 70309, 70310, 70311, 70312, 70313, 70314, 70315, 70316, 70317, 70318, 70319, 70320, 70321, 70322, 70323, 70324, 70325, 70326, 70327, 70328, 70329, 70330, 70331, 70332, 70333, 70334, 70335, 70336, 70337, 70338, 70339, 70340, 70341, 70342, 70343, 70344, 70345, 70346, 70347, 70348, 70349, 70350)

SELECT
       "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_superuser",
       "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email",
       "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."date_joined"
FROM "auth_user" WHERE "auth_user"."id" = 1 LIMIT 21


SELECT
       "posts_post"."id", "posts_post"."text", "posts_post"."pub_date", "posts_post"."author_id",
       "posts_post"."group_id", "posts_post"."image"
FROM "posts_post"
    INNER JOIN "auth_user" ON ("posts_post"."author_id" = "auth_user"."id")
    INNER JOIN "posts_follow" ON ("auth_user"."id" = "posts_follow"."author_id")
WHERE "posts_follow"."user_id" = 1000
ORDER BY "posts_post"."pub_date" DESC

