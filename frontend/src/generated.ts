import { TypedDocumentNode as DocumentNode } from '@graphql-typed-document-node/core';
export type Maybe<T> = T | null;
export type InputMaybe<T> = Maybe<T>;
export type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
export type MakeOptional<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]?: Maybe<T[SubKey]> };
export type MakeMaybe<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]: Maybe<T[SubKey]> };
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: string;
  String: string;
  Boolean: boolean;
  Int: number;
  Float: number;
};

export type Brew = {
  __typename?: 'Brew';
  brewer?: Maybe<SlackProfile>;
  created: Scalars['String'];
  id: Scalars['ID'];
  machine: Machine;
  modified: Scalars['String'];
  progress: Scalars['Int'];
  reactions: Array<BrewReaction>;
  status: Scalars['String'];
};

export type BrewReaction = {
  __typename?: 'BrewReaction';
  brew: Brew;
  emoji: Scalars['String'];
  id: Scalars['ID'];
  isCustomReaction: Scalars['Boolean'];
  reaction: Scalars['String'];
  user?: Maybe<SlackProfile>;
};

export type KitchenEvent = {
  __typename?: 'KitchenEvent';
  message: Scalars['String'];
  type: Scalars['String'];
};

export type Machine = {
  __typename?: 'Machine';
  avatarUrl: Scalars['String'];
  created: Scalars['String'];
  id: Scalars['ID'];
  lastBrew?: Maybe<Brew>;
  litersTotal: Scalars['Int'];
  modified: Scalars['String'];
  name: Scalars['String'];
  status: Scalars['String'];
};

export type Query = {
  __typename?: 'Query';
  machines: Array<Machine>;
  stats: Stats;
  users: Array<SlackProfile>;
};

export type SlackProfile = {
  __typename?: 'SlackProfile';
  displayName: Scalars['String'];
  image: Scalars['String'];
  imageOriginal: Scalars['String'];
  litersTotal: Scalars['Int'];
  realName: Scalars['String'];
  userId: Scalars['String'];
};


export type SlackProfileImageArgs = {
  size?: Scalars['Int'];
};

export type Stats = {
  __typename?: 'Stats';
  litersToday: Scalars['Int'];
  litersYesterday: Scalars['Int'];
};

export type Subscription = {
  __typename?: 'Subscription';
  connectToKitchenEvents: KitchenEvent;
};

export type ConnectToKitchenEventsSubscriptionVariables = Exact<{ [key: string]: never; }>;


export type ConnectToKitchenEventsSubscription = { __typename?: 'Subscription', connectToKitchenEvents: { __typename?: 'KitchenEvent', type: string, message: string } };

export type UserStatsQueryVariables = Exact<{ [key: string]: never; }>;


export type UserStatsQuery = { __typename?: 'Query', users: Array<{ __typename?: 'SlackProfile', userId: string, realName: string, displayName: string, imageOriginal: string, litersTotal: number, image48: string }> };

export type TodayStatsQueryVariables = Exact<{ [key: string]: never; }>;


export type TodayStatsQuery = { __typename?: 'Query', stats: { __typename?: 'Stats', litersToday: number, litersYesterday: number } };

export type MachinesQueryVariables = Exact<{ [key: string]: never; }>;


export type MachinesQuery = { __typename?: 'Query', machines: Array<{ __typename?: 'Machine', id: string, name: string, status: string, avatarUrl: string, litersTotal: number, lastBrew?: { __typename?: 'Brew', id: string, status: string, progress: number, created: string, modified: string, brewer?: { __typename?: 'SlackProfile', userId: string, realName: string, displayName: string, imageOriginal: string, image48: string } | null, reactions: Array<{ __typename?: 'BrewReaction', id: string, isCustomReaction: boolean, reaction: string, emoji: string }> } | null }> };


export const ConnectToKitchenEventsDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"subscription","name":{"kind":"Name","value":"ConnectToKitchenEvents"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"connectToKitchenEvents"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"type"}},{"kind":"Field","name":{"kind":"Name","value":"message"}}]}}]}}]} as unknown as DocumentNode<ConnectToKitchenEventsSubscription, ConnectToKitchenEventsSubscriptionVariables>;
export const UserStatsDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"UserStats"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"users"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"userId"}},{"kind":"Field","name":{"kind":"Name","value":"realName"}},{"kind":"Field","name":{"kind":"Name","value":"displayName"}},{"kind":"Field","name":{"kind":"Name","value":"imageOriginal"}},{"kind":"Field","alias":{"kind":"Name","value":"image48"},"name":{"kind":"Name","value":"image"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"size"},"value":{"kind":"IntValue","value":"48"}}]},{"kind":"Field","name":{"kind":"Name","value":"litersTotal"}}]}}]}}]} as unknown as DocumentNode<UserStatsQuery, UserStatsQueryVariables>;
export const TodayStatsDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"TodayStats"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"stats"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"litersToday"}},{"kind":"Field","name":{"kind":"Name","value":"litersYesterday"}}]}}]}}]} as unknown as DocumentNode<TodayStatsQuery, TodayStatsQueryVariables>;
export const MachinesDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"Machines"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"machines"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"name"}},{"kind":"Field","name":{"kind":"Name","value":"status"}},{"kind":"Field","name":{"kind":"Name","value":"avatarUrl"}},{"kind":"Field","name":{"kind":"Name","value":"litersTotal"}},{"kind":"Field","name":{"kind":"Name","value":"lastBrew"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"status"}},{"kind":"Field","name":{"kind":"Name","value":"progress"}},{"kind":"Field","name":{"kind":"Name","value":"created"}},{"kind":"Field","name":{"kind":"Name","value":"modified"}},{"kind":"Field","name":{"kind":"Name","value":"brewer"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"userId"}},{"kind":"Field","name":{"kind":"Name","value":"realName"}},{"kind":"Field","name":{"kind":"Name","value":"displayName"}},{"kind":"Field","name":{"kind":"Name","value":"imageOriginal"}},{"kind":"Field","alias":{"kind":"Name","value":"image48"},"name":{"kind":"Name","value":"image"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"size"},"value":{"kind":"IntValue","value":"48"}}]}]}},{"kind":"Field","name":{"kind":"Name","value":"reactions"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"id"}},{"kind":"Field","name":{"kind":"Name","value":"isCustomReaction"}},{"kind":"Field","name":{"kind":"Name","value":"reaction"}},{"kind":"Field","name":{"kind":"Name","value":"emoji"}}]}}]}}]}}]}}]} as unknown as DocumentNode<MachinesQuery, MachinesQueryVariables>;