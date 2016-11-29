#################################################################################################
# Author: Junyin Chen(jc2954), Yuxiao Kun(xy284), Zhenchuan Pang(zp55)
#
# Date: Nov.29 2016
#
# BCM2836Constants.py
#
# Description: Constants for BCM2836 SoC
#
# Reference:
# Datasheet of BCM2835
#
#################################################################################################

PERIPHERAL_LEN          = 0x002FFFFF

# Base Address
PERIPHERAL_BASE         = 0x3F000000
GPFSEL0_BASE            = 0x00200000
CM_GP0CTL_BASE          = 0x00101070
CM_GP0DIV_BASE          = 0x00101074

# Constants
GPFSEL0_FSEL4_MASK      = 0xFFFF8FFF
GPFSEL0_FSEL4_GPCLK0    = (0x001 << 14)
CM_GP0CTL_PASSWD        = (0x5a << 12)
CM_GP0CTL_MASH_1STAGE   = (0x01 << 9)
CM_GPOCTL_ENABLE        = (0x01 << 4)
CM_GP0CTL_SRC_PLLD      = (0x06)             # 500 MHz
PLLD_FREQ_MHZ           = 500.0
CM_GP0DIV_PASSWD        = (0x5a << 24)
CM_GP0DIV_DIVI_LSB      = 12
CM_GP0DIV_DIVF_MASK     = 0xFFFFF000
