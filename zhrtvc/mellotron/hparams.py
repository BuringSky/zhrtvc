# import tensorflow as tf
# from text.symbols import symbols
from aukit import Dict2Obj, hparams_griffinlim


def create_hparams(hparams_string=None, verbose=False, level=2):
    """Create model hyperparameters. Parse nondefault from given string."""

    # hparams = tf.contrib.training.HParams(
    hparams = Dict2Obj(dict(
        ################################
        # Experiment Parameters        #
        ################################
        epochs=1000000,
        iters_per_checkpoint=10000,  # 500,
        seed=1234,
        dynamic_loss_scaling=True,
        fp16_run=False,
        distributed_run=False,
        dist_backend="nccl",
        dist_url="tcp://localhost:54321",
        cudnn_enabled=True,
        cudnn_benchmark=False,
        ignore_layers=['speaker_embedding.weight'],

        ################################
        # Data Parameters             #
        ################################
        train_mode='train-f04',
        # f01:用基频；f02:用基频均值填充；f03:用零向量代替基频；f04:不用基频。
        # f01,f02,f03的模式都把prenet_f0_dim设为1，f04把prenet_f0_dim设为0。

        training_files=r"../../data/SV2TTS/mellotron/samples_ssml/train.txt",
        # 文件一行记录一个语音信息，每行的数据结构：数据文件夹名\t语音源文件\t文本\t说话人名称\n，样例如下：
        # 000000	Aibao/005397.mp3	他走近钢琴并开始演奏“祖国从哪里开始”。	0
        validation_files=r"../../data/SV2TTS/mellotron/samples_ssml/validation.txt",
        # 'filelists/ljs_audiopaths_text_sid_val_filelist.txt',
        text_cleaners='ssml',  # ['chinese_cleaners'],
        p_arpabet=1.0,
        cmudict_path=None,  # "data/cmu_dictionary",

        ################################
        # Audio Parameters             #
        ################################
        max_wav_value=32768.0,
        sampling_rate=hparams_griffinlim.sample_rate,  # 16000,  # 22050,
        filter_length=hparams_griffinlim.n_fft,  # 1024,
        hop_length=hparams_griffinlim.hop_size,  # 256,
        win_length=hparams_griffinlim.win_size,  # 1024,
        n_mel_channels=401,  # 80,
        mel_fmin=0.0,
        mel_fmax=8000.0,
        f0_min=80,
        f0_max=880,
        harm_thresh=0.25,

        ################################
        # Model Parameters             #
        ################################
        n_symbols=145,  # len(symbols),
        symbols_embedding_dim=128 * level,  # 512,

        # Encoder parameters
        encoder_kernel_size=5,
        encoder_n_convolutions=3,
        encoder_embedding_dim=128 * level,  # 512,

        # Decoder parameters
        n_frames_per_step=1,  # currently only 1 is supported
        decoder_rnn_dim=256 * level,  # 1024,
        prenet_dim=64 * level,  # 256,
        prenet_f0_n_layers=1,
        prenet_f0_dim=0,  # 1, 如果不启用f0，则设置为0。
        prenet_f0_kernel_size=1,
        prenet_rms_dim=0,
        prenet_rms_kernel_size=1,
        max_decoder_steps=2000,  # 1000,
        gate_threshold=0.5,
        p_attention_dropout=0.1,
        p_decoder_dropout=0.1,
        p_teacher_forcing=1.0,

        # Attention parameters
        attention_rnn_dim=256 * level,  # 1024,
        attention_dim=32 * level,  # 128,

        # Location Layer parameters
        attention_location_n_filters=8 * level,  # 32,
        attention_location_kernel_size=31,

        # Mel-post processing network parameters
        postnet_embedding_dim=128 * level,  # 512,
        postnet_kernel_size=5,
        postnet_n_convolutions=5,

        # Speaker embedding
        n_speakers=123,
        speaker_embedding_dim=16 * level,  # 32 * level,  # 128,

        # Reference encoder
        with_gst=False,  # True,
        ref_enc_filters=[8 * level, 8 * level, 16 * level, 16 * level, 32 * level, 32 * level],
        # [32, 32, 64, 64, 128, 128],
        ref_enc_size=[3, 3],
        ref_enc_strides=[2, 2],
        ref_enc_pad=[1, 1],
        ref_enc_gru_size=32 * level,  # 128,

        # Style Token Layer
        token_embedding_size=0,  # 64 * level,  # 256,  # 如果with_gst=False，则手动改为0。
        token_num=10,
        num_heads=8,

        ################################
        # Optimization Hyperparameters #
        ################################
        use_saved_learning_rate=False,
        learning_rate=1e-3,
        learning_rate_min=1e-5,
        learning_rate_anneal=50000,
        weight_decay=1e-6,
        grad_clip_thresh=1.0,
        batch_size=32,  # 32,
        mask_padding=True,  # set model's padded outputs to padded values

    ))

    if hparams_string:
        # tf.compat.v1.logging.info('Parsing command line hparams: %s', hparams_string)
        hparams.parse(hparams_string)

    # if verbose:
    #     tf.compat.v1.logging.info('Final parsed hparams: %s', hparams.values())

    return hparams
