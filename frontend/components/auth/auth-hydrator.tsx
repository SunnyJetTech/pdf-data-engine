"use client";

import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { useAppSelector } from "@/store/hooks";
import { getProfile } from "@/api/auth.api";
import { setUser, clearUser, setHydrated, setInitialized,} from "@/store/slices/authSlice";

export default function AuthHydrator() {
  const dispatch = useDispatch();

  const initialized = useAppSelector(
    (state) => state.auth.initialized
  );

  useEffect(() => {
    console.log(
      "AUTH HYDRATOR EFFECT"
    );

    if (initialized) {
      console.log(
        "AUTH HYDRATOR SKIPPED"
      );
      return;
    }

    hydrate();
  }, [initialized]);

  async function hydrate() {
    console.log("HYDRATE START");

    try {
      const response =
        await getProfile();

      console.log(
        "PROFILE RESPONSE",
        response
      );

      if (
        response?.status ===
          "success" &&
        response?.data
      ) {
        dispatch(
          setUser(response.data)
        );
      } else {
        dispatch(clearUser());
      }
    } catch (error) {
      console.log(
        "PROFILE ERROR",
        error
      );

      dispatch(clearUser());
    } finally {
      dispatch(setHydrated());

      dispatch(
        setInitialized()
      );

      console.log(
        "HYDRATE END"
      );
    }
  }

  return null;
}