type SlackProfile = {
  userId: string;
  displayName?: string;
  realName?: string;
  imageOriginal?: string;
  image48?: string;
};
type BrewReaction = {
  id: number;
  reaction: string;
  isCustomReaction: boolean;
  emoji: string;
  user: SlackProfile;
};

type Brew = {
  id: number;
  status: string;
  progress: number;
  brewer?: SlackProfile;
  modified: string;
  created: string;
  reactions: BrewReaction[];
};

type Machine = {
  id: number;
  name: string;
  status: string;
  avatarUrl: string;
  lastBrew?: Brew;
  modified: string;
  created: string;
};

type TopUser = {
  litersTotal: number;
} & SlackProfile;
