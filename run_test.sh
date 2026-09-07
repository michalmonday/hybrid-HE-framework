cd ~/coding/hybrid-HE-framework/thirdparty/tfhe/build \
&& make -j4 \
&& make install \
&& cd ../../../build \
&& make -j4 \
&& ./tests/my_basic_algorithm_tfhe_test
