"""
Python unit tests for FractionalizeNFT
"""
import pytest
from brownie import Contract, ERC20Factory, FractionalizeNFT, TestNFT, accounts


@pytest.fixture(scope="class")
def nft_contract(deployer_address):
    nft_contract = deployer_address.deploy(TestNFT)
    return nft_contract


@pytest.fixture(scope="class")
def mint_nft(nft_contract, deployer_address, user_address):
    tx = nft_contract.mintNFT(user_address, "www.foo.xyz", {"from": deployer_address})
    return tx


@pytest.fixture(scope="class")
def nft_id(mint_nft):
    return mint_nft.return_value


class TestTestNFT:
    def test_mint_nft(self, nft_contract, nft_id, user_address):
        assert user_address == nft_contract.ownerOf(nft_id)

    def test_transfer_nft(self, nft_id, nft_contract, user_address):
        receiver_address = accounts[2]
        nft_contract.safeTransferFrom(user_address, receiver_address, nft_id, {"from": user_address})
        assert receiver_address == nft_contract.ownerOf(nft_id)


class TestFractionalizeNFT:
    @pytest.fixture(scope="class")
    def erc20_name(self):
        return "Woof coin"

    @pytest.fixture(scope="class")
    def erc20_symbol(self):
        return "Woof"

    @pytest.fixture(scope="class")
    def erc20_supply(self):
        return 100

    @pytest.fixture(scope="class")
    def frac_contract(self, deployer_address):
        return deployer_address.deploy(FractionalizeNFT)

    @pytest.fixture(scope="class", autouse=True)
    def create_fractionalized_nft(
        self, frac_contract, nft_contract, nft_id, user_address, erc20_name, erc20_symbol, erc20_supply
    ):
        nft_contract.approve(frac_contract.address, nft_id, {"from": user_address})
        tx = frac_contract.fractionalizeNft(
            nft_contract, nft_id, erc20_name, erc20_symbol, erc20_supply, {"from": user_address}
        )
        return tx

    @pytest.fixture
    def erc20_contract(self, create_fractionalized_nft):
        erc20_address = create_fractionalized_nft.return_value
        return Contract.from_abi("foo", erc20_address, ERC20Factory.abi)

    # TODO: Implement reasonable test of receive function
    def test_receive(self, user_address, frac_contract):
        user_address.transfer(frac_contract.address, "1 ether")

    # TODO: Implement test of fallback function
    @pytest.mark.xfail
    def test_fallback(self):
        assert 0, "unimplemented"

    def test_erc20_total_supply(self, erc20_contract, erc20_supply):
        assert erc20_contract.totalSupply() == erc20_supply

    def test_erc20_initial_balance(self, erc20_contract, user_address, erc20_supply):
        assert erc20_contract.balanceOf(user_address) == erc20_supply

    def test_erc20_name(self, erc20_contract, erc20_name):
        assert erc20_contract.name() == erc20_name

    def test_erc20_symbol(self, erc20_contract, erc20_symbol):
        assert erc20_contract.symbol() == erc20_symbol

    def test_nft_owner(self, nft_contract, nft_id, frac_contract):
        assert nft_contract.ownerOf(nft_id) == frac_contract.address
