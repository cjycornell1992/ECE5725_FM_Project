#################################################################
# Author: Junyin Chen(jc2954), Yuxiao Kun(xy284), Zhenchuan Pang(zp55)
#
# Date: Nov.10 2016
#
# SI4703Constants.py
#
# Description: Constants for Si4703-C19, mainly for Registers
# Reference: https://cdn.sparkfun.com/assets/learn_tutorials/2/7/4/Si4703_datasheet.pdf
################################################################

SI4703_I2C_ADDR                            = 0x10
SI4703_REG_NUM                             = 16    # 16 registers in total, each register 2 bytes
SI4703_RD_ADDR_START                       = 0x0A  # read starts from 0x0A
SI4703_WR_ADDR_START                       = 0x02  # write starts from 0x02
SI4703_REGION_LIST                         = ['USA','EU','JPN','JPN+']

#######################################################################
################ Device ID and Manufacture ID info Reg ################
#######################################################################

# Reg Addr
SI4703_DEVICE_ID_ADDR                      = 0x0000
# Mask
SI4703_DEVICE_ID_PN_MASK                   = 0b1111000000000000
SI4703_DEVICE_ID_MFGID_MASK                = 0b0000111111111111
# LSB
SI4703_DEVICE_ID_PN_LSB                    = 12
SI4703_DEVICE_ID_MFGID_LSB                 = 0
# Values
SI4703_DEVICE_ID                           = 0x01
SI4703_MANUFACTURE_ID                      = 0x242

#######################################################################
################            Chip ID info Reg           ################
#######################################################################

# Reg Addr
SI4703_CHIP_ID_ADDR                        = 0x0001
# Mask
SI4703_CHIP_ID_REV_MASK                    = 0b1111110000000000
SI4703_CHIP_ID_DEV_MASK                    = 0b0000001111000000
SI4703_CHIP_ID_FIRMWARE_MASK               = 0b0000000000111111
# LSB
SI4703_CHIP_ID_REV_LSB                     = 10
SI4703_CHIP_ID_DEV_LSB                     = 6
SI4703_CHIP_ID_FIRMWARE_LSB                = 0
# Values
SI4703_CHIP_ID_REV_C                       = 0x04
SI4703_CHIP_ID_DEV_BEFORE_UP               = 0x8
SI4703_CHIP_ID_DEV_AFTER_UP                = 0x9
SI4703_CHIP_ID_FIRMWARE_BEFORE_UP          = 0x00
SI4703_CHIP_ID_FIRMWARE_AFTER_UP           = 0x13

#######################################################################
################        Power Configuration Reg        ################
#######################################################################

# Reg Addr 
SI4703_POWER_CONFIG_ADDR                   = 0x0002
# Mask
SI4703_POWER_CONFIG_DSMUTE_MASK            = 0b1000000000000000
SI4703_POWER_CONFIG_DMUTE_MASK             = 0b0100000000000000
SI4703_POWER_CONFIG_MONO_MASK              = 0b0010000000000000
SI4703_POWER_CONFIG_RDSM_MASK              = 0b0000100000000000
SI4703_POWER_CONFIG_SKMODE_MASK            = 0b0000010000000000
SI4703_POWER_CONFIG_SEEKUP_MASK            = 0b0000001000000000
SI4703_POWER_CONFIG_SEEK_MASK              = 0b0000000100000000
SI4703_POWER_CONFIG_DISABLE_MASK           = 0b0000000001000000
SI4703_POWER_CONFIG_ENABLE_MASK            = 0b0000000000000001
# LSB
SI4703_POWER_CONFIG_DSMUTE_LSB             = 15
SI4703_POWER_CONFIG_DMUTE_LSB              = 14
SI4703_POWER_CONFIG_MONO_LSB               = 13
SI4703_POWER_CONFIG_RDSM_LSB               = 11
SI4703_POWER_CONFIG_SKMODE_LSB             = 10
SI4703_POWER_CONFIG_SEEKUP_LSB             = 9
SI4703_POWER_CONFIG_SEEK_LSB               = 8
SI4703_POWER_CONFIG_DISABLE_LSB            = 6
SI4703_POWER_CONFIG_ENABLE_LSB             = 0
# Values
SI4703_POWER_CONFIG_DSMUTE_EN              = 0
SI4703_POWER_CONFIG_DSMUTE_DIS             = 1
SI4703_POWER_CONFIG_DMUTE_EN               = 0
SI4703_POWER_CONFIG_DMUTE_DIS              = 1
SI4703_POWER_CONFIG_MONO_DEFAULT           = 0
SI4703_POWER_CONFIG_MONO_FORCE             = 1
SI4703_POWER_CONFIG_RDSM_STANDARD          = 0
SI4703_POWER_CONFIG_RDSM_VERBOSE           = 1
SI4703_POWER_CONFIG_SKMODE_DEFAULT         = 0
SI4703_POWER_CONFIG_SKMODE_UPPER_LOWER     = 1
SI4703_POWER_CONFIG_SEEKUP_DOWN            = 0
SI4703_POWER_CONFIG_SEEKUP_UP              = 1
SI4703_POWER_CONFIG_SEEK_DIS               = 0
SI4703_POWER_CONFIG_SEEK_EN                = 1
SI4703_POWER_CONFIG_DISABLE_LOW            = 0
SI4703_POWER_CONFIG_DISABLE_HIGH           = 1
SI4703_POWER_CONFIG_ENABLE_LOW             = 0
SI4703_POWER_CONFIG_ENABLE_HIGH            = 1

#######################################################################
################              Channel Reg              ################
#######################################################################

# Reg Addr 
SI4703_CHANNEL_ADDR                        = 0x0003
# Mask
SI4703_CHANNEL_TUNE_MASK                   = 0b1000000000000000
SI4703_CHANNEL_CHAN_MASK                   = 0b0000001111111111
# LSB
SI4703_CHANNEL_TUNE_LSB                    = 15
SI4703_CHANNEL_CHAN_LSB                    = 0
# Values
""" For US, Freq = 0.2 (MHz) x Channel + 87.5 MHz """
SI4703_CHANNEL_TUNE_DIS                    = 0
SI4703_CHANNEL_TUNE_EN                     = 1

#######################################################################
################     System Configuration Reg1         ################
#######################################################################

# Reg Addr 
SI4703_SYS_CONFIG1_ADDR                    = 0x0004
# Mask
SI4703_SYS_CONFIG1_RDSIEN_MASK             = 0b1000000000000000
SI4703_SYS_CONFIG1_STCIEN_MASK             = 0b0100000000000000
SI4703_SYS_CONFIG1_RDS_MASK                = 0b0001000000000000
SI4703_SYS_CONFIG1_DE_MASK                 = 0b0000100000000000
SI4703_SYS_CONFIG1_AGCD_MASK               = 0b0000010000000000
SI4703_SYS_CONFIG1_BLNDADJ_MASK            = 0b0000000011000000
SI4703_SYS_CONFIG1_GPIO3_MASK              = 0b0000000000110000
SI4703_SYS_CONFIG1_GPIO2_MASK              = 0b0000000000001100
SI4703_SYS_CONFIG1_GPIO1_MASK              = 0b0000000000000011
# LSB
SI4703_SYS_CONFIG1_RDSIEN_LSB              = 15
SI4703_SYS_CONFIG1_STCIEN_LSB              = 14
SI4703_SYS_CONFIG1_RDS_LSB                 = 12
SI4703_SYS_CONFIG1_DE_LSB                  = 11
SI4703_SYS_CONFIG1_AGCD_LSB                = 10
SI4703_SYS_CONFIG1_BLNDADJ_LSB             = 6
SI4703_SYS_CONFIG1_GPIO3_LSB               = 4
SI4703_SYS_CONFIG1_GPIO2_LSB               = 2
SI4703_SYS_CONFIG1_GPIO1_LSB               = 0
# Values
SI4703_SYS_CONFIG1_RDSIEN_DIS              = 0x00
SI4703_SYS_CONFIG1_RDSIEN_EN               = 0x01
SI4703_SYS_CONFIG1_STCIEN_DIS              = 0x00
SI4703_SYS_CONFIG1_STCIEN_EN               = 0x01
SI4703_SYS_CONFIG1_RDS_DIS                 = 0x00
SI4703_SYS_CONFIG1_RDS_EN                  = 0x01
SI4703_SYS_CONFIG1_DE_USA                  = 0x00    # 75us
SI4703_SYS_CONFIG1_DE_OTHER                = 0x01    # 50us, Europe, Australia, Japan
SI4703_SYS_CONFIG1_AGCD_EN                 = 0x00
SI4703_SYS_CONFIG1_AGCD_DIS                = 0x01
SI4703_SYS_CONFIG1_BLNDADJ_DEFAULT         = 0x00    # 31-49 RSSI dBuV
SI4703_SYS_CONFIG1_BLNDADJ_6DB             = 0x01    # 37-55 RSSI dBuV
SI4703_SYS_CONFIG1_BLNDADJ_MINUS_12DB      = 0x02    # 19-37 RSSI dBuV
SI4703_SYS_CONFIG1_BLNDADJ_MINUS_6DB       = 0x03    # 25-43 RSSI dBuV
SI4703_SYS_CONFIG1_GPIO3_Z                 = 0x00
SI4703_SYS_CONFIG1_GPIO3_ST                = 0x01
SI4703_SYS_CONFIG1_GPIO3_LOW               = 0x02
SI4703_SYS_CONFIG1_GPIO3_HIGH              = 0x03
SI4703_SYS_CONFIG1_GPIO2_Z                 = 0x00
SI4703_SYS_CONFIG1_GPIO2_INT               = 0x01
SI4703_SYS_CONFIG1_GPIO2_LOW               = 0x02
SI4703_SYS_CONFIG1_GPIO2_HIGH              = 0x03
SI4703_SYS_CONFIG1_GPIO1_Z                 = 0x00
SI4703_SYS_CONFIG1_GPIO1_LOW               = 0x02
SI4703_SYS_CONFIG1_GPIO1_HIGH              = 0x03

SI4703_DE_DIC = {'USA':SI4703_SYS_CONFIG1_DE_USA, 'EU':SI4703_SYS_CONFIG1_DE_OTHER,
                 'JPN':SI4703_SYS_CONFIG1_DE_OTHER, 'JPN+':SI4703_SYS_CONFIG1_DE_OTHER}

#######################################################################
################     System Configuration Reg2         ################
#######################################################################

# Reg Addr 
SI4703_SYS_CONFIG2_ADDR                    = 0x0005
# Mask
SI4703_SYS_CONFIG2_SEEKTH_MASK             = 0b1111111100000000
SI4703_SYS_CONFIG2_BAND_MASK               = 0b0000000011000000
SI4703_SYS_CONFIG2_SPACE_MASK              = 0b0000000000110000
SI4703_SYS_CONFIG2_VOLUME_MASK             = 0b0000000000001111
# LSB
SI4703_SYS_CONFIG2_SEEKTH_LSB              = 8
SI4703_SYS_CONFIG2_BAND_LSB                = 6
SI4703_SYS_CONFIG2_SPACE_LSB               = 4
SI4703_SYS_CONFIG2_VOLUME_LSB              = 0
# Values
SI4703_SYS_CONFIG2_SEEKTH_MIN              = 0x00
SI4703_SYS_CONFIG2_SEEKTH_MAX              = 0x7F
SI4703_SYS_CONFIG2_SEEKTH_RECOMMENDED      = 0x19
SI4703_SYS_CONFIG2_BAND_USA                = 0x00     # 87.5 - 108 MHz
SI4703_SYS_CONFIG2_BAND_EUROPE             = 0x00     # 87.5 - 108 MHz
SI4703_SYS_CONFIG2_BAND_JAPAN_WIDE         = 0x01     # 76   - 108 MHz
SI4703_SYS_CONFIG2_BAND_JAPAN              = 0x02     # 76   - 90  MHz
SI4703_SYS_CONFIG2_SPACE_USA               = 0x00     # 200 kHz
SI4703_SYS_CONFIG2_SPACE_AUSTRALIA         = 0x00     # 200 kHz
SI4703_SYS_CONFIG2_SPACE_EUROPE            = 0x01     # 100 kHz
SI4703_SYS_CONFIG2_SPACE_JAPAN             = 0x01     # 100 kHz
SI4703_SYS_CONFIG2_SPACE_50K               = 0x02     # 50  kHz
SI4703_SYS_CONFIG2_VOLUME_MAX              = 0xf      # 4-bit DAC

SI4703_BAND_DIC  = {'USA':SI4703_SYS_CONFIG2_BAND_USA, 'EU':SI4703_SYS_CONFIG2_BAND_EUROPE,
                   'JPN':SI4703_SYS_CONFIG2_BAND_JAPAN, 'JPN+':SI4703_SYS_CONFIG2_BAND_JAPAN_WIDE}

SI4703_SPACE_DIC = {'USA':SI4703_SYS_CONFIG2_SPACE_USA, 'EU':SI4703_SYS_CONFIG2_SPACE_EUROPE,
                    'JPN':SI4703_SYS_CONFIG2_SPACE_JAPAN, 'JPN+':SI4703_SYS_CONFIG2_SPACE_JAPAN}

#######################################################################
################     System Configuration Reg3         ################
#######################################################################

# Reg Addr 
SI4703_SYS_CONFIG3_ADDR                    = 0x0006
# Mask
SI4703_SYS_CONFIG3_SMUTER_MASK             = 0b1100000000000000
SI4703_SYS_CONFIG3_SMUTEA_MASK             = 0b0011000000000000
SI4703_SYS_CONFIG3_VOLEXT_MASK             = 0b0000000100000000
SI4703_SYS_CONFIG3_SKSNR_MASK              = 0b0000000011110000
SI4703_SYS_CONFIG3_SKCNT_MASK              = 0b0000000000001111
# LSB
SI4703_SYS_CONFIG3_SMUTER_LSB              = 14
SI4703_SYS_CONFIG3_SMUTEA_LSB              = 12
SI4703_SYS_CONFIG3_VOLEXT_LSB              = 8
SI4703_SYS_CONFIG3_SKSNR_LSB               = 4
SI4703_SYS_CONFIG3_SKCNT_LSB               = 0
# Values
SI4703_SYS_CONFIG3_SMUTER_FASTEST          = 0x00
SI4703_SYS_CONFIG3_SMUTER_FAST             = 0x01
SI4703_SYS_CONFIG3_SMUTER_SLOW             = 0x02
SI4703_SYS_CONFIG3_SMUTER_SLOWEST          = 0x03
SI4703_SYS_CONFIG3_SMUTEA_16DB             = 0x00
SI4703_SYS_CONFIG3_SMUTEA_14DB             = 0x01
SI4703_SYS_CONFIG3_SMUTEA_12DB             = 0x02
SI4703_SYS_CONFIG3_SMUTEA_10DB             = 0x03
SI4703_SYS_CONFIG3_VOLEXT_DIS              = 0
SI4703_SYS_CONFIG3_VOLEXT_EN               = 1
SI4703_SYS_CONFIG3_SKSNR_DIS               = 0x00
SI4703_SYS_CONFIG3_SKSNR_MIN               = 0x01
SI4703_SYS_CONFIG3_SKSNR_MAX               = 0x07
SI4703_SYS_CONFIG3_SKSNR_RECOMMENDED       = 0x04
SI4703_SYS_CONFIG3_SKCNT_DIS               = 0x00
SI4703_SYS_CONFIG3_SKCNT_MAX               = 0x01
SI4703_SYS_CONFIG3_SKCNT_MIN               = 0x0f
SI4703_SYS_CONFIG3_SKCNT_RECOMMENDED       = 0x08

#######################################################################
################             Test Reg 1                ################
#######################################################################

# Reg Addr 
SI4703_TEST1_ADDR                          = 0x0007
# Mask
SI4703_TEST1_XOSCEN_MASK                   = 0b1000000000000000
SI4703_TEST1_AHIZEN_MASK                   = 0b0100000000000000
# LSB
SI4703_TEST1_XOSCEN_LSB                    = 15
SI4703_TEST1_AHIZEN_LSB                    = 14
# Values
SI4703_TEST1_XOSCEN_DIS                    = 0
SI4703_TEST1_XOSCEN_EN                     = 1
SI4703_TEST1_AHIZEN_DIS                    = 0
SI4703_TEST1_AHIZEN_EN                     = 1

#######################################################################
################             Test Reg 2                ################
#######################################################################

# Reg Addr 
SI4703_TEST2_ADDR                          = 0x0008

#######################################################################
################      Boot Configuration Reg           ################
#######################################################################

# Reg Addr 
SI4703_BOOT_CONFIG_ADDR                    = 0x0009

#######################################################################
################          Status RSSI Reg              ################
#######################################################################

# Reg Addr 
SI4703_STATUS_RSSI_ADDR                    = 0x000A
# Mask
SI4703_STATUS_RSSI_RDSR_MASK               = 0b1000000000000000
SI4703_STATUS_RSSI_STC_MASK                = 0b0100000000000000
SI4703_STATUS_RSSI_SFBL_MASK               = 0b0010000000000000
SI4703_STATUS_RSSI_AFCRL_MASK              = 0b0001000000000000
SI4703_STATUS_RSSI_RDSS_MASK               = 0b0000100000000000
SI4703_STATUS_RSSI_BLERA_MASK              = 0b0000011000000000
SI4703_STATUS_RSSI_ST_MASK                 = 0b0000000100000000
SI4703_STATUS_RSSI_RSSI_MASK               = 0b0000000011111111
# LSB
SI4703_STATUS_RSSI_RDSR_LSB                = 15
SI4703_STATUS_RSSI_STC_LSB                 = 14
SI4703_STATUS_RSSI_SFBL_LSB                = 13
SI4703_STATUS_RSSI_AFCRL_LSB               = 12
SI4703_STATUS_RSSI_RDSS_LSB                = 11
SI4703_STATUS_RSSI_BLERA_LSB               = 9
SI4703_STATUS_RSSI_ST_LSB                  = 8
SI4703_STATUS_RSSI_RSSI_LSB                = 0
# Values
SI4703_STATUS_RSSI_RDSR_NONE               = 0
SI4703_STATUS_RSSI_RDSR_RDY                = 1
SI4703_STATUS_RSSI_STC_PENDING             = 0
SI4703_STATUS_RSSI_STC_COMPLETE            = 1
SI4703_STATUS_RSSI_SFBL_SUCCESS            = 0
SI4703_STATUS_RSSI_SFBL_FAIL               = 1
SI4703_STATUS_RSSI_AFCRL_NOT_RAILED        = 0
SI4703_STATUS_RSSI_AFCRL_RAILED            = 1
SI4703_STATUS_RSSI_RDSS_NOT_SYNC           = 0
SI4703_STATUS_RSSI_RDSS_SYNC               = 1
SI4703_STATUS_RSSI_BLERA_NONE              = 0x00
SI4703_STATUS_RSSI_BLERA_FEW               = 0x01
SI4703_STATUS_RSSI_BLERA_SOME              = 0x02
SI4703_STATUS_RSSI_BLERA_MANY              = 0x03
SI4703_STATUS_RSSI_ST_MONO                 = 0
SI4703_STATUS_RSSI_ST_STEREO               = 0
SI4703_STATUS_RSSI_RSSI_MIN                = 0x00 # 0 (increment 1 dBuV)
SI4703_STATUS_RSSI_RSSI_MAX                = 0xff # 75 dB

#######################################################################
################          Read Channel Reg             ################
#######################################################################

# Reg Addr
SI4703_READ_CHANNEL_ADDR                   = 0x000B
# Mask
SI4703_READ_CHANNEL_BLERB_MASK             = 0b1100000000000000
SI4703_READ_CHANNEL_BLERC_MASK             = 0b0011000000000000
SI4703_READ_CHANNEL_BLERD_MASK             = 0b0000110000000000
SI4703_READ_CHANNEL_READCHAN_MASK          = 0b0000001111111111
# LSB
SI4703_READ_CHANNEL_BLERB_LSB              = 14
SI4703_READ_CHANNEL_BLERC_LSB              = 12
SI4703_READ_CHANNEL_BLERD_LSB              = 10
SI4703_READ_CHANNEL_READCHAN_LSB           = 0
# Values
SI4703_READ_CHANNEL_BLERB_NONE             = 0x00
SI4703_READ_CHANNEL_BLERB_FEW              = 0x01
SI4703_READ_CHANNEL_BLERB_SOME             = 0x02
SI4703_READ_CHANNEL_BLERB_MANY             = 0x03
SI4703_READ_CHANNEL_BLERC_NONE             = 0x00
SI4703_READ_CHANNEL_BLERC_FEW              = 0x01
SI4703_READ_CHANNEL_BLERC_SOME             = 0x02
SI4703_READ_CHANNEL_BLERC_MANY             = 0x03
SI4703_READ_CHANNEL_BLERD_NONE             = 0x00
SI4703_READ_CHANNEL_BLERD_FEW              = 0x01
SI4703_READ_CHANNEL_BLERD_SOME             = 0x02
SI4703_READ_CHANNEL_BLERD_MANY             = 0x03
""" For US, Freq = 0.2 (MHz) x Channel + 87.5 MHz 
READCHAN[9:0] provides the current tuned channel and is updated during a seek
operation and after a seek or tune operation completes """

#######################################################################
################               RDSA Reg                ################
#######################################################################

# Reg Addr
SI4703_RDSA_ADDR                           = 0x000C
# Mask
SI4703_RDSA_MASK                           = 0xffff
# LSB
SI4703_RDSA_BLERB_LSB                      = 0
# Values: 16 bits block A Data

#######################################################################
################               RDSB Reg                ################
#######################################################################

# Reg Addr
SI4703_RDSB_ADDR                           = 0x000D
# Mask
SI4703_RDSB_MASK                           = 0xffff
# LSB
SI4703_RDSB_BLERB_LSB                      = 0
# Values: 16 bits block B Data

#######################################################################
################               RDSC Reg                ################
#######################################################################

# Reg Addr
SI4703_RDSC_ADDR                           = 0x000E
# Mask
SI4703_RDSC_MASK                           = 0xffff
# LSB
SI4703_RDSC_BLERB_LSB                      = 0
# Values: 16 bits block C Data

#######################################################################
################               RDSD Reg                ################
#######################################################################

# Reg Addr
SI4703_RDSD_ADDR                           = 0x000F
# Mask
SI4703_RDSD_MASK                           = 0xffff
# LSB
SI4703_RDSD_BLERB_LSB                      = 0
# Values: 16 bits block D Data

