type BrewReaction = {
  id: number;
  reaction: string;
  isCustomReaction: boolean;
  emoji: string;
};

type Brew = {
  id: number;
  status: string;
  progress: number;
  brewerSlackUsername: string;
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
