import { useMutation } from "@apollo/client";
import { LOGOUT_MUTATION } from "@/lib/apollo";
import { Button } from "./button";

export const Logout = () => {
  const [logoutMutation] = useMutation(LOGOUT_MUTATION);

  return (
    <div className="border border-border w-1/2 flex flex-col gap-3 p-4">
      <Button onClick={() => logoutMutation()}>Logout</Button>
    </div>
  );
};
