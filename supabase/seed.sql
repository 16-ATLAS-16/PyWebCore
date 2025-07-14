CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY NOT NULL UNIQUE REFERENCES auth.users ON DELETE CASCADE,
    firstName VARCHAR(30) NOT NULL,
    lastName VARCHAR(30) NOT NULL,
    displayName VARCHAR(30) NOT NULL,
    email VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS public.roles (
    role_id INTEGER PRIMARY KEY NOT NULL UNIQUE,
    role_name VARCHAR(25) NOT NULL,
    role_weight INT DEFAULT 0,
    role_state INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS public.user_roles (
    id UUID PRIMARY KEY NOT NULL UNIQUE REFERENCES public.users,
    role_id INTEGER NOT NULL REFERENCES public.roles,
    last_updated TIMESTAMPTZ
);

CREATE OR REPLACE FUNCTION public.user_has_role(in_user_uuid uuid, in_role_id INTEGER)
RETURNS BOOLEAN
LANGUAGE 'plpgsql' STABLE
AS $$
  DECLARE out_user_has_role integer;
  BEGIN
    SELECT 1
    INTO out_user_has_role
    FROM public.user_roles
    WHERE
          user_roles.user_uuid = in_user_uuid
      AND user_roles.role_id = in_role_id;
  END
$$;

ALTER FUNCTION public.user_has_role(uuid, INTEGER) OWNER TO postgres;
GRANT EXECUTE ON FUNCTION public.user_has_role(uuid, INTEGER) TO anon;
GRANT EXECUTE ON FUNCTION public.user_has_role(uuid, INTEGER) TO authenticated;
GRANT EXECUTE ON FUNCTION public.user_has_role(uuid, INTEGER) TO postgres;
GRANT EXECUTE ON FUNCTION public.user_has_role(uuid, INTEGER) TO public;
GRANT EXECUTE ON FUNCTION public.user_has_role(uuid, INTEGER) TO service_role;
