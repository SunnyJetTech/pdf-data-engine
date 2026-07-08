import { createSlice, PayloadAction,} from "@reduxjs/toolkit";

interface AuthState {
  user: any | null;
  hydrated: boolean;
  loading: boolean;
  initialized: boolean;
}

const initialState: AuthState = {
  user: null,
  hydrated: false,
  loading: true,
  initialized: false,
};

const authSlice = createSlice({
  name: "auth",

  initialState,

  reducers: {
    setUser: (
      state,
      action: PayloadAction<any>
    ) => {
      state.user = action.payload;
    },

    clearUser: (state) => {
      state.user = null;
    },

    setHydrated: (state) => {
      state.hydrated = true;
      state.loading = false;
    },

    setInitialized: (state) => {
      state.initialized = true;
    },

    setLoading: (
      state,
      action: PayloadAction<boolean>
    ) => {
      state.loading = action.payload;
    },
  },
});

export const {
  setUser,
  clearUser,
  setHydrated,
  setInitialized,
  setLoading,
} = authSlice.actions;

export default authSlice.reducer;