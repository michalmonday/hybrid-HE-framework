#pragma once

#include <bitset>
#include <string>
#include <vector>

#include "../../common/Cipher.h"

namespace MY_BASIC_ALGORITHM {

// Blockcipher just for testing a plaintext/ciphertext with specific size
constexpr BlockCipherParams MY_BASIC_ALGORITHM_PARAMS = {16, 128, 6, 46, 6, 46};

constexpr unsigned STATE_SIZE = 288;
constexpr unsigned IV_SIZE = MY_BASIC_ALGORITHM_PARAMS.key_size_bits;

typedef std::bitset<STATE_SIZE> stateblock;
typedef std::bitset<IV_SIZE> ivblock;
typedef std::bitset<MY_BASIC_ALGORITHM_PARAMS.key_size_bits> keyblock;

class My_Basic_Algorithm : public BlockCipher {
 public:
  My_Basic_Algorithm(std::vector<uint8_t> secret_key)
      : BlockCipher(MY_BASIC_ALGORITHM_PARAMS, secret_key) {}

  virtual ~My_Basic_Algorithm() = default;

  virtual std::string get_cipher_name() const { return "MY_BASIC_ALGORITHM"; }
  virtual std::vector<uint8_t> encrypt(std::vector<uint8_t> plaintext,
                                       size_t bits) const;
  virtual std::vector<uint8_t> decrypt(std::vector<uint8_t> ciphertext,
                                       size_t bits) const;

  virtual void prep_one_block() const;

 private:
  std::vector<uint8_t> keystream(const keyblock& key, const ivblock& iv,
                                 size_t bits) const;
  void init(const keyblock& key, const ivblock& iv, stateblock& state,
            ivblock& inner_iv, keyblock& inner_key) const;
};

}  // namespace MY_BASIC_ALGORITHM
