# NFT Fractionalizer

## Motivation and Aim

It seems extremely likely that NFTs (non-fungible tokens) will become ubiquitous in many aspects of our digital (and
physical) world in the mid to long-term future. As NFTs become more widely adopted, multiple parties may wish to share
ownership of a single NFT. Dividing the ownership of NFTs is possible on smart programming platforms by locking the NFT
in a contract in return for a specified quantity of tokens that each represent partial ownership of the locked
NFT. These tokens may then be distributed to multiple accounts. This process is known as "fractionalization" of an
NFT. The aim of this project is to implement a simple EVM-based dapp (decentralized application) that allows a user to
fractionalize their [ERC721](https://ethereum.org/en/developers/docs/standards/tokens/erc-721) NFTs into
[ERC20](https://ethereum.org/en/developers/docs/standards/tokens/erc-20/) tokens.

## Workflow: Contract Actions and Participants

Actions:
1. Fractionalize: An **NFT owner** can __fractionalize__ their NFT by transferring the NFT to the contract. In
  return the NFT owner receives the entire supply of a newly created ERC20 token that they specified at
  fractionalization. The **NFT Owner** also sets an initial buyout price for the NFT at fractionalization.
2. Buyout: A **buyer** can __buyout__ (__purchase__) the locked NFT by transferring (at least) the specified amount
   of ETH to the contract. The NFT gets transferred to the **buyer's** account.
3. Claim: Following a buyout, an **ERC20 token holder** of a fractionalized NFT can __claim__ their share of the **buyout** price received
   from the **buyer** as determined by the proportion of the ERC20 token supply that they hold. This is also referred to
   as a **payout** in the frontend.
4. Redeem: The **holder of all ERC20 tokens** can __redeem__ the NFT by sending all of the the ERC20 tokens to the
  contract; the NFT is transferred to the redeeming account. Redemption allows the holder of all the tokens to
  "unfractionalize" the NFT. The most practical use case is that the original owner decided they no longer wanted to
  fractionalize the NFT.

As a side effect, the above functionality also allows the dapp to act as a simple marketplace (or escrow) for accounts to sell NFTs in exchange for ether.

## Bootcamp Requirements

### [Design Patterns Decisions](design_pattern_decisions.md)

### [Avoiding Attack Vectors and Bugs](avoiding_common_attacks.md)

### [Deployed Address](deployed_address.txt)

### Directory Structure

* `.github/workflows`: For github actions (currently the contracts are compiled and unit-tested automatically).
* `client`: Frontend for the FractionalizeNFT contract.
* `docs`: Additional documentation.
* `contracts`: FractionalizeNFT and helper smart contracts.
* `tests`: Python unit tests (executed via brownie).

### Compile, Deploy and Test the Contracts Locally

#### Requirements

* Node.js >= v14.
* gananche-cli.
* Python >= 3.6 (during development mainly 3.8 and 3.9 were used).
* brownie and the Python package dependencies given in [requirements.txt](./requirements.txt).

#### Brownie Installation

```
python3 -m venv venv  # Create a local virtual environment to install packages in.
source venv/bin/activate  # Bash, activate scripts for shells available in same folder.
pip install --upgrade pip
pip install -r requirements.txt
```

#### Compile, Deploy and Unit Test

The contracts are compiled and tested upon push in Github CI.

To run the tests locally run `brownie test` (this will start ganache-cli for you):
```
source venv/bin/activate  # If virtual environment not already activated
brownie test
```
Or, with gas profiling and coverage enabled (slower):
```
brownie test --gas --coverage
```

#### Deploying for Manual Testing

The `scripts/deploy.py` script can be used to deploy the contracts locally and populate the FractionalizeNFT contract with some NFTs
ready for manual testing:
1. Start the console:
  ```
  source venv/bin/activate  # If virtual environment not already activated
  brownie console
  ```
2. From within the console, run:
  ```python
  nft_contract, frac_contract = run("deploy", "main_dev")
  ```
#### Configuring Local Accounts (Optional)

A mnemonic may be added to `.env` in the form
```
MNEMONIC=YOUR MNEMONIC ... PHRASE HERE
```
This mnemonic value will be used in the brownie config and applied when starting ganache-cli.

### Running the Frontend Locally

Note: See "Deploying for Manual Testing" for how to deploy the contract and populate it with fractionalized NFTs ready
for use with the frontend.

1. Run:
   ```
   cd client
   yarn install 
   yarn start
   ```
2. Open [http://localhost:3000](http://localhost:3000).


### Deploy the Contracts to the Ropsten Test Network

Deploy to Ropsten (and verify source code via Etherscan):
```
brownie run deploy.py --network ropsten
```
Source code verification additionally requires:
* An Etherscan API token `.env` entry in the form:
  ```
  ETHERSCAN_TOKEN=<TOKEN>
  ```
* Brownie >= 1.17.0.

### Ethereum Address for NFT Certification

`0x7b13c2F7AaA8C772Bd0a13A86B0CF633fAf790B0` (danceratopz.eth)

### Possible Improvements

Solidity:
* Feature: Allow an ERC20 token holder to update the buyout price weighted by the proportion of the ERC20 token supply that they hold.
* Feature: Delete an entry from `fracNFTs` if it is no longer in use, i.e., when:
  * An NFT has been redeemed, or
  * An NFT has been bought and there are no pending payouts (the contract holds the entire supply of the corresponding ERC20 token).
* Chore: Improve unit test coverage.
* Chore: Implement as an upgradable contract.

Frontend:
* Refactor: Remove inline styling (to CSS).
* Feature: Allow a user to open a detailed view of a fractionalized NFT to display its full and account-specific information
  (e.g., percentage of ERC20 tokens held).
* Feature: Add a pager for the Listings on the Market, Redeem and Payout.
* Feature: Render Listings on the Market, Redeem and Payout pages asynchronously.
* Fix: Improve/optimise image loading.
* Feature: Make use of emitted events from the smart contract.
* Feature/Clean-up: Remove the Redeem page. It can be incorporated in the Market, or the potential "Detail" view as a "Redeem" or "Cancel" button.
* Chore: Add unit tests.
* Chore: Upgrade packages.
