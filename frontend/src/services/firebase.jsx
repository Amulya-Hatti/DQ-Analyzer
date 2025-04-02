// import { initializeApp } from "firebase/app";
// import { 
//   getAuth, 
//   signInWithPopup, 
//   GoogleAuthProvider,
//   createUserWithEmailAndPassword,
//   signInWithEmailAndPassword
// } from "firebase/auth";

// const firebaseConfig = {
//   apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
//   authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
//   projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
//   storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
//   messagingSenderId: import.meta.env.VITE_FIREBASE_SENDER_ID,
//   appId: import.meta.env.VITE_FIREBASE_APP_ID
// };

// const app = initializeApp(firebaseConfig);
// export const auth = getAuth(app);

// export const signInWithGoogle = async () => {
//   try {
//     const provider = new GoogleAuthProvider();
//     const result = await signInWithPopup(auth, provider);
//     return result.user;
//   } catch (error) {
//     throw new Error(error.message);
//   }
// };

// export const signInWithEmail = async (email, password, isLogin) => {
//   try {
//     if (isLogin) {
//       await signInWithEmailAndPassword(auth, email, password);
//     } else {
//       await createUserWithEmailAndPassword(auth, email, password);
//     }
//   } catch (error) {
//     throw new Error(error.message);
//   }
// };

import { initializeApp } from "firebase/app";
import { 
  getAuth, 
  signInWithPopup, 
  GoogleAuthProvider,
  signInWithEmailAndPassword
} from "firebase/auth";

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);

export const signInWithGoogle = async () => {
  try {
    const provider = new GoogleAuthProvider();
    const result = await signInWithPopup(auth, provider);
    return result.user;
  } catch (error) {
    console.error("Google Sign-In Error:", error.message);
    throw new Error("Google authentication failed. Please try again.");
  }
};

export const signInWithEmail = async (email, password) => {
  try {
    await signInWithEmailAndPassword(auth, email, password);
  } catch (error) {
    console.error("Email Authentication Error:", error.code, error.message);

    switch (error.code) {
      case "auth/operation-not-allowed":
        throw new Error("Email/Password sign-in is not enabled. Enable it in Firebase Console.");
      case "auth/user-not-found":
        throw new Error("No account found with this email. Please check your credentials.");
      case "auth/wrong-password":
        throw new Error("Incorrect password. Please try again.");
      case "auth/invalid-credential":
        throw new Error("Invalid email or password. Check your credentials.");
      default:
        throw new Error("Login failed. Please try again.");
    }
  }
};

